# VSCode add-on for generating python docstrings with an LLM backend

### Important: You need to run an LLM instance for this add-on to work. See *Usage* below.

Visual Studio Code extension to quickly generate docstrings for python functions
using AI(NLP) technology. This project is forked from
[graykode/ai-docstring](https://github.com/graykode/ai-docstring). Main
difference is that this version uses a quantized version of
[Mistral-AI](https://mistral.ai)'s 7B model and *attempts* to produce a complete
docstring including variable types and descriptions according to the chosen 
template.  

Demo (real time, using Google Colab T4 runtime as backend):

https://github.com/burakbudanur/llmdocstring/assets/1861787/414a9728-548b-49e9-afde-da9938bdde54

## Docstring Formats

-   Google (default)
-   docBlockr
-   Numpy
-   Sphinx

## Usage

### Backend:

#### (1) ngrok & google colab solution

1. Create [ngrok](https://ngrok.com) and [google colab](https://colab.research.google.com) accounts.
2. Open the [server notebook](server/llmserver.ipynb) on google colab.
3. Replace `<authtoken>` with your ngrok authtoken in the second cell and uncomment the corresponding line
4. Run all cells
5. Copy the ngrok address (without https) into the extension settings `llmdocstring.ServerEndpoint`

#### (2) local 

1. Recommended: Create a new python environment with python version 3.9 and activate
2. In the directory `server`, run `pip install -r requirements.txt`
3. Check [llama-cpp-python installation page](https://pypi.org/project/llama-cpp-python/) to install llama-cpp-python according to your hardware.
4. Run `python llmserver.py`
5. Copy `127.0.0.1:5000` into the extension settings `llmdocstring.ServerEndpoint`

### on vscode:

Cursor must be on the line directly below the definition to generate full auto-populated docstring

-   Press enter after opening docstring with triple quotes (`"""` or `'''`)
-   Keyboard shortcut: `ctrl+shift+2` or `cmd+shift+2` for mac
    -   Can be changed in Preferences -> Keyboard Shortcuts -> extension.generateDocstring
-   Command: `Generate Docstring`
-   Right click menu: `Generate Docstring`
