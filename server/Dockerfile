FROM python:3.12.2
RUN wget -P /app/weights/ https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q6_K.gguf
COPY . /app/
WORKDIR /app
RUN pip install -r requirements.txt
CMD python llmserver.py
