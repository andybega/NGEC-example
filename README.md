# NGEC Install Testing

Testing whether NGEC can be installed on different systems, using [uv](https://docs.astral.sh/uv/). 

Python version targest are 3.11 and greater. 

One precondition is that there is no virtual environment setup, and also without an existing uv project. The code below can be used to clean up uv artifacts and a local `.venv/`. 

```
deactivate 2>/dev/null || true
bash ./reset_env.sh
```

On Windows:

```pwsh
deactivate
.\reset_env.ps1
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

|    OS   | Device | Transformers | vLLM | mlx | 
|---------|--------|--------------|------|-----|
| Linux   | CPU    | [link](#linux-with-cpu-and-transformers) | [3] | - |
|         | GPU    | [link](#linux-with-gpu-and-transformers) | [link](#linux-with-gpu-and-vllm) | - |
| macOS   | CPU    | [1] | [1] | [1] |
|         | MPS    | [link](#macos-with-mps-and-transformers) | - | [link](#macos-with-mps-and-mlx) |
| Windows | CPU    | [link](#windows-with-cpu-and-transformers) | [3] | - |
|         | GPU    | [link](#windows-with-gpu-and-transformers) | [2] | - |

\- = not possible  
1: All Apple Silicon Macs have MPS; older Intel Macs with CPU not supported.  
2: vLLM does not natively support Windows GPU, https://docs.vllm.ai/en/stable/getting_started/installation/gpu/.  
3: Theoretically it might be possible to run vLLM CPU, but not clear there's a benefit over transformers. 


## macOS with MPS and transformers

```sh
uv init --python 3.13 
uv venv --seed
source .venv/bin/activate

uv add torch torchvision
uv run check_mps.py

uv add git+https://github.com/ahalterman/NGEC-2025 --extra models

uv run main.py --mps
```

## macOS with MPS and mlx


```sh
uv init --python 3.13 
uv venv --seed
source .venv/bin/activate

uv add torch torchvision
uv run check_mps.py

uv add git+https://github.com/ahalterman/NGEC-2025 --extra models --extra mlx

uv run main.py --backend mlx
```


## Windows with CPU and transformers


```powershell
uv init --python 3.13 
uv venv --seed
.venv\Scripts\Activate

uv add torch torchvision 
uv run check_cpu.py

uv add git+https://github.com/ahalterman/NGEC-2025 --extra models

uv run main.py 
```


## Windows with GPU and transformers


```powershell
uv init --python 3.13 
uv venv --seed
.venv\Scripts\Activate

# Adjust for CUDA version
uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cu130
uv run check_gpu.py

uv add git+https://github.com/ahalterman/NGEC-2025 --extra models

uv run main.py --gpu
```



## Windows with GPU and vllm

Technically not supported.

```powershell
uv init --python 3.13 
uv venv --seed
.venv\Scripts\Activate

# Adjust based on CUDA version
uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cu130
# Test this works
uv run check_gpu.py

uv add git+https://github.com/ahalterman/NGEC-2025 --extra models --extra vllm

uv run main.py --gpu --backend vllm 
```

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

```
uv init --python 3.13 
uv venv --seed
source .venv/bin/activate

# The torch Linux version is GPU by default, so need special index
# Ideally add to project.toml, see https://docs.astral.sh/uv/guides/integration/pytorch/#configuring-accelerators-with-optional-dependencies
uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
uv run check_cpu.py

uv add git+https://github.com/ahalterman/NGEC-2025 --extra models 

uv run main.py 
```





