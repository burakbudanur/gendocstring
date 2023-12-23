import os
import threading
from datetime import datetime
from flask import Flask, jsonify, request
import time
import json
from pathlib import Path
from huggingface_hub import hf_hub_download
import multiprocessing
import re

try:
    from llama_cpp import Llama
except: 
    print(
        "Cannot find llama_cpp. Visit \n" 
        "https://llama-cpp-python.readthedocs.io/en/latest/#installation-with-specific-hardware-acceleration-blas-cuda-metal-etc \n"
        " for installation instructions for your hardware."
          )

num_cpu = multiprocessing.cpu_count()
print(num_cpu)

def log(string):
    now = datetime.now()

    print("now =", now)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    f = open("gendocstring.log", "a")
    f.write(dt_string + '\n')
    f.close()

    with open("gendocstring.log","a") as f:
        f.writelines(string)
        
        
def download_weights():
    weights_dir = Path("weights")
    weights_dir.mkdir(exist_ok=True)

    repo_id = "TheBloke/Mistral-7B-Instruct-v0.1-GGUF"
    filename = "mistral-7b-instruct-v0.1.Q6_K.gguf"

    if (weights_dir / Path(filename)).exists():
        print(
            f"{filename} exists. Delete manually if you wish to download again."
            )
        return
    else:
        print(
            "Downloading the weights. This will take some time and disk space."
            "Next run will be faster."
            )        
        return hf_hub_download(
            repo_id = repo_id, filename=filename, local_dir='./weights/',
            local_dir_use_symlinks = False
            )


def get_docstring_from_template(code, template):

    instruction = "According to the template, produce a docstring for the "
    instruction += "following python function."
    instruction += "Return the full function definition with the docstring."

    message = f"Docstring template: \n {template} \n <s>[INST] {instruction} [/INST]</s> \n {code}"
    output = llm(message, echo=True, stream=False, max_tokens=4096)
    text = output['choices'][0]['text']
    print(text)
    docstring_pattern = re.compile(r'\'\'\'(.*?)\'\'\'|\"\"\"(.*?)\"\"\"', re.DOTALL)
    match = docstring_pattern.search(text)

    return match.groups()[1] if match else "Docstring generation failed, please try again."


if __name__ == '__main__':
    
    download_weights()
    
    model = "weights/mistral-7b-instruct-v0.1.Q6_K.gguf"  # instruction model
    llm = Llama(
        model_path=model, n_ctx=10240, n_batch=256, n_threads=num_cpu,
        n_gpu_layers=-1, verbose=True, seed=42
        )

    app = Flask(__name__)
    port = "5000"

    # Define Flask routes
    @app.route("/")
    def index():
        return "Hello from gendocstring server."

    @app.route("/summary", methods=["POST"])
    def summary():
        if request.method == "POST":
            payload = request.get_json()
            t0 = time.time()

            # Generate docstring here

            code = payload["code"]
            snippet = payload["snippet"]
            template = snippet.replace('\"\"\"\n', '')

            log("code:")
            log(code)
            log("snippet:")
            log(snippet)

            docstring = get_docstring_from_template(code, template)                
            
            if docstring[0:1] == '\n':
                docstring = docstring[1:]
            docstring = docstring.rstrip()+'\n'

            log(docstring)

            t1 = time.time()
            result = {
                'message' : [docstring],
                'time' : (t1 - t0),
                'device' : "computer",
                'length' : len(docstring)
            }

            return jsonify(**result)

    # Start the Flask server in a new thread
    threading.Thread(target=app.run, kwargs={"use_reloader": False}).start()