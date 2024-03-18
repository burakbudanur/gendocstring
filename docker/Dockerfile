FROM ubuntu:23.10 as ubuntu_apk
RUN apt update

FROM ubuntu_apk as temp_git
RUN apt install git -y
RUN git clone https://github.com/burakbudanur/llmdocstring.git /tmp/llmdocstring

FROM ubuntu_apk as temp_wget
RUN apt install wget -y
RUN wget -P /app/weights/ https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q6_K.gguf

FROM ubuntu_apk
RUN apt install python3-pip -y
COPY --from=temp_git /tmp/llmdocstring/server /app
COPY --from=temp_wget /app/weights/ /app/weights/
WORKDIR /app
RUN pip install -r requirements.txt --break-system-packages
RUN pip install llama-cpp-python==0.2.56 --break-system-packages
CMD python3 llmserver.py
