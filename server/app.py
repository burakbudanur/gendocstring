# Copyright 2020-present Tae Hwan Jung
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json
import time
import torch
import argparse
import torch.nn as nn
from model import Seq2Seq
from flask import Flask, jsonify, request
from utils import Example, convert_examples_to_features, logger
from transformers import RobertaConfig, RobertaModel, RobertaTokenizer
from torch.utils.data import TensorDataset, DataLoader, SequentialSampler

app = Flask(__name__)


def inference(data):
    # Calculate bleu
    eval_sampler = SequentialSampler(data)
    eval_dataloader = DataLoader(data, sampler=eval_sampler, batch_size=len(data))

    args.model.eval()
    p = []
    for batch in eval_dataloader:
        batch = tuple(t.to(args.device) for t in batch)
        source_ids, source_mask = batch
        with torch.no_grad():
            preds = args.model(source_ids=source_ids, source_mask=source_mask)
            for pred in preds:
                t = pred[0].cpu().numpy()
                t = list(t)
                if 0 in t:
                    t = t[: t.index(0)]
                text = args.tokenizer.decode(t, clean_up_tokenization_spaces=False)
                p.append(text)
    return (p, source_ids.shape[-1])


def get_features(examples):
    features = convert_examples_to_features(
        examples, args.tokenizer, args, stage="test"
    )
    all_source_ids = torch.tensor(
        [f.source_ids[: args.max_source_length] for f in features], dtype=torch.long
    )
    all_source_mask = torch.tensor(
        [f.source_mask[: args.max_source_length] for f in features], dtype=torch.long
    )
    return TensorDataset(all_source_ids, all_source_mask)


def build_model(model_class, config, tokenizer):
    encoder = model_class(config=config)
    decoder_layer = nn.TransformerDecoderLayer(
        d_model=config.hidden_size, nhead=config.num_attention_heads
    )
    decoder = nn.TransformerDecoder(decoder_layer, num_layers=6)
    model = Seq2Seq(
        encoder=encoder,
        decoder=decoder,
        config=config,
        beam_size=args.beam_size,
        max_length=args.max_target_length,
        sos_id=tokenizer.cls_token_id,
        eos_id=tokenizer.sep_token_id,
    )

    assert os.path.exists("pytorch_model.bin"), "Weight is not downloaded."

    model.load_state_dict(
        torch.load(
            "pytorch_model.bin",
            map_location=torch.device("cpu"),
        ),
        strict=False,
    )
    return model


def create_app():
    @app.route("/")
    def index():
        return jsonify(hello="world")

    @app.route("/summary", methods=["POST"])
    def summary():
        if request.method == "POST":
            payload = request.get_json()
            example = [
                Example(
                    source=payload["code"],
                    target=None,
                )
            ]

            t0 = time.time()
            message, length = inference(data=get_features(example))
            t1 = time.time()
            result = {
                'message' : message,
                'time' : (t1 - t0),
                'device' : args.device_name,
                'length' : length
            }
            logger.info(json.dumps(result, indent=4))
            return jsonify(**result)

    @app.route("/tokenizer", methods=["POST"])
    def tokenizer():
        if request.method == "POST":
            payload = request.get_json()
            tokens = args.tokenizer.tokenize(payload["code"])
            return jsonify(tokens=tokens)

    return app


def main(args):
    config = RobertaConfig.from_pretrained("microsoft/codebert-base")
    args.tokenizer = RobertaTokenizer.from_pretrained(
        "microsoft/codebert-base", do_lower_case=False
    )

    args.model = build_model(
        model_class=RobertaModel, config=config, tokenizer=args.tokenizer
    ).to(args.device)

    app = create_app()
    app.run(host=args.host, debug=True, port=args.port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "--max_source_length",
        default=512,
        type=int,
        help="The maximum total source sequence length after tokenization. Sequences longer "
        "than this will be truncated, sequences shorter will be padded.",
    )
    parser.add_argument(
        "--max_target_length",
        default=128,
        type=int,
        help="The maximum total target sequence length after tokenization. Sequences longer "
        "than this will be truncated, sequences shorter will be padded.",
    )
    parser.add_argument(
        "--beam_size", default=10, type=int, help="beam size for beam search"
    )
    parser.add_argument("--no_cuda", action='store_true', help="Avoid using CUDA when available")

    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5000)

    args = parser.parse_args()

    args.device_name = "cuda" if torch.cuda.is_available() and not args.no_cuda else "cpu"
    args.device = torch.device(args.device_name)
    args.beam_size = (args.beam_size if torch.cuda.is_available() and not args.no_cuda else 1)

    logger.info(args)

    main(args)
