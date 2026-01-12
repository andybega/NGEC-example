# NGEC Install Testing

Testing whether NGEC can be installed on different systems, using [uv](https://docs.astral.sh/uv/). 

Python version targest are 3.11 and greater. 

One precondition is that there is no virtual environment setup, and also without an existing uv project. The code below can be used to clean up uv artifacts and a local `.venv/`. 

```
deactivate 2>/dev/null || true
bash ./reset_env.sh
```

The tests in `main.py` depend on these two environment variables, fill in the correct info and make sure they are set:

```
export ES_USER="<fill this in>"
export ES_PASSWORD="<fill this in>"
```

After that, the basic steps are:

1. Initialize a uv project and venv. 
2. Install PyTorch with uv, using the correct platform-specific invocation. 
3. Install NGEC from GitHub, using the the correct platform-specific extras.
4. Run the `main.py` tests (with the correct CLI arguments); it will print tests results.

`main.py` needs arguments so that it adjusts the tests based on platform:

```bash
uv run main.py --help
```

```
usage: main.py [-h] [--backend {transformers,vllm,mlx}] [--gpu] [--mps]

Test NGEC installation

options:
  -h, --help            show this help message and exit
  --backend {transformers,vllm,mlx}
                        Backend to use (default: transformers)
  --gpu                 Enable GPU
  --mps                 Enable MPS
```

Platform specific install commands are below. 

## macOS with MPS and transformers

```
uv init --python 3.13 
uv venv --seed
source .venv/bin/activate

uv add torch torchvision
uv run check_mps.py

uv add git+https://github.com/ahalterman/NGEC-2025 --extra models

uv run main.py --mps
```

## macOS with MPS and mlx


```
uv init --python 3.13 
uv venv --seed
source .venv/bin/activate

uv add torch torchvision
uv run check_mps.py

uv add git+https://github.com/ahalterman/NGEC-2025 --extra models --extra mlx

uv run main.py --backend mlx
```


## Windows with CPU and transformers


```
uv init --python 3.13 
uv venv --seed
source .venv/bin/activate

# Task 1: this next line needs to be verified
uv add torch torchvision
# Test this works
uv run check_cpu.py

uv add git+https://github.com/ahalterman/NGEC-2025 --extra models

uv run main.py 
```

## Windows with GPU and transformers


```
uv init --python 3.13 
uv venv --seed
source .venv/bin/activate

# Task 1: this next line needs to be verified
# Probably wrong
uv add torch torchvision
# Test this works
uv run check_gpu.py

uv add git+https://github.com/ahalterman/NGEC-2025 --extra models

uv run main.py --gpu
```


## Windows with CPU and vllm

```
uv init --python 3.13 
uv venv --seed
source .venv/bin/activate

# Task 1: this next line needs to be verified
uv add torch torchvision
# Test this works
uv run check_gpu.py

uv add git+https://github.com/ahalterman/NGEC-2025 --extra models --extra vllm

uv run main.py --backend vllm 
```

## Windows with GPU and vllm


## Linux with GPU and transformers

```
uv init --python 3.13 
uv venv --seed
source .venv/bin/activate

# Task 1: this next line needs to be verified
# I think this works with CUDA 12.8?
uv add torch torchvision
# Test this works
uv run check_gpu.py

uv add git+https://github.com/ahalterman/NGEC-2025 --extra models 

uv run main.py --gpu
```

## Linux with GPU and vllm

```
uv init --python 3.13 
uv venv --seed
source .venv/bin/activate

# Task 1: this next line needs to be verified
# I think this works with CUDA 12.8?
uv add torch torchvision
# Test this works
uv run check_gpu.py

uv add git+https://github.com/ahalterman/NGEC-2025 --extra models --extra vllm

uv run main.py --gpu --backend vllm
```

## Linux with CPU and transformers


## Linux with CPU and vllm


## macOS with CPU and transformers

Not sure there even is an option for macOS CPU

## macOS with CPU and mlx

Not sure there even is an option for macOS CPU


