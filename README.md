# ShelfAware

![ShelfAware](shelfaware.png)


## Running

export OPENAI_BASE_URL=http://hugger:8000/v1

### Install dependencies
```sh
conda create -n shelfaware python=3.10
conda activate shelfaware

pip3 install -e .
```

### Run NIM Service for LLM

https://docs.nvidia.com/nim/large-language-models/latest/getting-started.html
https://docs.nvidia.com/nim/nemo-retriever/text-embedding/latest/support-matrix.html

Get your `NGC_API_KEY` per https://docs.nvidia.com/ngc/gpu-cloud/ngc-user-guide/index.html#ngc-api-keys

```sh
$ docker login nvcr.io
Username: $oauthtoken
Password: <PASTE_API_KEY_HERE>
```

Passing `--gpus` all to docker run is acceptable in homogeneous environments with 1 or more of the same GPU.

```sh
nvidia-smi -L
```

This is working on my RTX4090
21538MiB VRAM Usage


`--max-model-len 40960` is crucial for managing memory on consumer-end GPUs.

`--gpus '"device=1"'` might be needed if you have multiple and want to run specific models on specific GPUs.

```sh
export NGC_API_KEY=<PASTE_API_KEY_HERE>
export LOCAL_NIM_CACHE=~/.cache/nim
export NIM_MODEL_PROFILE=vllm-fp16-tp1
export SHELFAWARE_MODEL=llama-3.1-8b-instruct:1.1.2

mkdir -p "$LOCAL_NIM_CACHE"

docker run -it --rm \
    --gpus '"device=1"' \
    --shm-size=16GB \
    -e NGC_API_KEY \
    -e NIM_MODEL_PROFILE \
    -e NIM_SERVED_MODEL_NAME="$SHELFAWARE_MODEL" \
    -v "$LOCAL_NIM_CACHE:/opt/nim/.cache" \
    -u $(id -u) \
    -p 8000:8000 \
    nvcr.io/nim/meta/llama-3.1-8b-instruct:1.1.2 \
    python3 -m vllm_nvext.entrypoints.openai.api_server --max-model-len 40960
```

### Run NIM for text embeddings

https://docs.nvidia.com/nim/nemo-retriever/text-embedding/latest/getting-started.html

I run it on my second GPU - RTX4060
1244MiB VRAM Usage

```sh
export NGC_API_KEY=<PASTE_API_KEY_HERE>
export LOCAL_NIM_CACHE=~/.cache/nim
export SHELFAWARE_MODEL_EMBEDDINGS=nvidia/nv-embedqa-e5-v5
export IMG_NAME="nvcr.io/nim/$SHELFAWARE_MODEL_EMBEDDINGS:1.0.0"
mkdir -p "$LOCAL_NIM_CACHE"

# Start the NIM
docker run -it --rm --name=nim-embeddings \
  --runtime=nvidia \
  --gpus '"device=0"' \
  --shm-size=16GB \
  -e NGC_API_KEY \
  -v "$LOCAL_NIM_CACHE:/opt/nim/.cache" \
  -p 8010:8000 \
  $IMG_NAME

#  -u $(id -u) \
```

### Vision

https://docs.vllm.ai/en/latest/models/vlm.html

```sh
export NGC_API_KEY=<PASTE_API_KEY_HERE>
export LOCAL_NIM_CACHE=~/.cache/nim
export NIM_MODEL_PROFILE=vllm-fp16-tp1
export SHELFAWARE_MODEL=llama-3.1-8b-instruct:1.1.2
export SHELFAWARE_MODEL_VISION=microsoft/phi-3-vision-128k-instruct
mkdir -p "$LOCAL_NIM_CACHE"

# Start the NIM
docker run -it --rm \
    --gpus '"device=1"' \
    --shm-size=16GB \
    -e NGC_API_KEY \
    -e NIM_SERVED_MODEL_NAME="$SHELFAWARE_MODEL_VISION" \
    -v "$LOCAL_NIM_CACHE:/opt/nim/.cache" \
    -u $(id -u) \
    -p 8020:8000 \
    nvcr.io/nim/meta/llama-3.1-8b-instruct:1.1.2 \
    python3 -m vllm_nvext.entrypoints.openai.api_server --max-model-len 40960 --model $SHELFAWARE_MODEL_VISION
```


### Models

https://docs.nvidia.com/nim/large-language-models/1.1.0/models.html
https://docs.nvidia.com/nim/nemo-retriever/text-embedding/latest/support-matrix.html


### Troubleshooting GPUs

```sh
$ docker run -it --rm     --gpus '"device=1"'     --shm-size=16GB     -e NGC_API_KEY     -v "$LOCAL_NIM_CACHE:/opt/nim/.cache"     -u $(id -u)     -p 8000:8000     nvcr.io/nim/meta/llama-3.1-8b-instruct:1.1.2 list-model-profiles
```

# TODO:
tools
docker-compose to launch everything

Instrumentation:
OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED


---

from openfoods.client import OpenFoodClient

client = OpenFoodClient()
product = client.fetch_product("4099100207149")

if product:
    print(product.product_name)
    client.fetch_image(product)
