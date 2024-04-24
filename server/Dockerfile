FROM python:3.9.18
RUN wget -P /app/weights/ https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf
COPY . /app/
WORKDIR /app
RUN CMAKE_ARGS="-DLLAMA_CLBLAST=on" pip install -r requirements.txt
CMD python llmserver.py
