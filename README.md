# VSCode add-on for generating python docstrings with an LLM backend



Visual Studio Code extension to quickly generate docstrings for python functions
using AI(NLP) technology. This project is forked from
[graykode/ai-docstring](https://github.com/graykode/ai-docstring). Main
difference is that this version uses a quantized version of
[Mistral-AI][https://mistral.ai]'s 7B model and *attempts* to produce full
docstring including variable types and descriptions according to the chosen 
template.  

## Docstring Formats

-   Google (default)
-   docBlockr
-   Numpy
-   Sphinx
-   PEP0257 (coming soon)

<video width="640" src="https://github.com/burakbudanur/llmdocstring/blob/6b4af53c1b001bb50046e34a2a31f5d9c82cbb79/demo.mp4" autoplay></video>

## Usage

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


This project is licensed under the [Apache 2.0 License](LICENSE) which is based on MIT License.
