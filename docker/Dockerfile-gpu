FROM nvcr.io/nvidia/cuda:10.0-cudnn7-runtime-ubuntu18.04
LABEL maintainer="nlkey2022@gmail.com"

RUN DEBIAN_FRONTEND=noninteractive apt-get -qq update \
 && DEBIAN_FRONTEND=noninteractive apt-get -qqy install curl python3-pip git \
 && rm -rf /var/lib/apt/lists/*

ARG PYTORCH_WHEEL="https://download.pytorch.org/whl/cu101/torch-1.6.0%2Bcu101-cp36-cp36m-linux_x86_64.whl"
ARG WEIGHT="1YrkwfM-0VBCJaa9NYaXUQPODdGPsmQY4"

RUN git clone https://github.com/graykode/ai-docstring.git /app/ai-docstring \
    && cd /app/ai-docstring/server

WORKDIR /app/ai-docstring/server

RUN pip3 install ${PYTORCH_WHEEL} gdown
RUN gdown https://drive.google.com/uc?id=${WEIGHT}

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "app.py"]