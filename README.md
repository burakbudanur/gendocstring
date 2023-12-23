# VSCode add-on for generating python docstrings with an LLM backend



Visual Studio Code extension to quickly generate docstrings for python functions
using AI(NLP) technology. This project is forked from
[graykode/ai-docstring](https://github.com/graykode/ai-docstring). Main
difference is that this version uses a quantized version of
[Mistral-AI][https://mistral.ai]'s 7B model and *attempts* to produce full
docstring including variable types and descriptions according to the chosen 
template.  

![Auto Generate Docstrings](images/demo.gif)

## Features

-   AI Quickly generate a docstring snippet that can be tabbed through.
-   Choose between several different types of docstring formats.
-   Infers parameter types through pep484 type hints, default values, and var names.
-   Support for args, kwargs, decorators, errors, and parameter types

## Docstring Formats

-   Google (default)
-   docBlockr
-   Numpy
-   Sphinx
-   PEP0257 (coming soon)

## Usage

Usage is very simple. You just (1) run the container for the model inference server and (2) install extension in vscode and use.

#### (1) Run the container for the model inference server

1. If you have GPU machine : `docker run -it -d --gpus 0 -p 5000:5000 graykode/ai-docstring:gpu`, after installing [nvidia-docker](https://github.com/NVIDIA/nvidia-docker). 
2. If you have only CPU : 
 a. Run flask server with [google colab and ngrok](server/server.ipynb)(Recommend!) 
 or b. use docker cpu image : `docker run -it -d -p 5000:5000 graykode/ai-docstring:cpu`
    - At this time, it is very likely to cause OOM problem. We need more memory limit than roughly 2GB.
    So add `--memory 2g --memory-swap` parameter in linux and change memory limit in `Preferences > Advanced` more than 2GB(default) in macOS.

#### (2) Install extension in vscode and use

Cursor must be on the line directly below the definition to generate full auto-populated docstring

-   Press enter after opening docstring with triple quotes (`"""` or `'''`)
-   Keyboard shortcut: `ctrl+shift+2` or `cmd+shift+2` for mac
    -   Can be changed in Preferences -> Keyboard Shortcuts -> extension.generateDocstring
-   Command: `Generate Docstring`
-   Right click menu: `Generate Docstring`

## Extension Settings

Extension Settings are the same as the [mother project](https://github.com/NilsJPWerner/autoDocstring#extension-settings) except for `autoDocstring.ServerEndpoint` :
-   `ai-docstring.ServerEndpoint`: endpoint address accessible to the server.

## About training and dataset

For training data, [github/CodeSearchNet](https://github.com/github/CodeSearchNet) was used, and as an initial model, we used Code2NL(Code to Natural Language) fine-tuning tasks in [microsoft/CodeBERT](https://github.com/microsoft/CodeBERT). For detailed instructions, refer to the paper ([CodeBERT: A Pre-Trained Model for Programming and Natural Languages](https://arxiv.org/pdf/2002.08155.pdf)) and [this section](https://github.com/microsoft/CodeBERT#fine-tune-1).

## Inference Benchmark(mean of 100 trials)
| Device | beam_size | max_source_length |  max_target_length | Time(ms) |
| :-----:| :---: | :---:| :---: | :---: |
| CPU    | 1    | 256   | 128   | 470  |
| CPU    | 10   | 256   | 128   | 1332 |
| CPU    | 1    | 512   | 128   | 511  |
| CPU    | 10   | 512   | 128   | 1954 |
| GPU    | 1    | 256   | 128   | 165  |
| GPU    | 10   | 256   | 128   | 381  |
| GPU    | 1    | 512   | 128   | 205  |
| GPU    | 10   | 512   | 128   | 545  |
- CPU : Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz
- GPU : Nvidia Tesla T4

## License

This project is licensed under the [Apache 2.0 License](LICENSE) which is based on MIT License.
