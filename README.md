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

Known issue; don't run yet

```powershell
uv init --python 3.13 
uv venv --seed
.venv\Scripts\Activate

# Task 1: this next line needs to be verified
uv add torch torchvision 
# Test this works
uv run check_cpu.py

uv add git+https://github.com/ahalterman/NGEC-2025 --extra models

uv run main.py 
```

```
Detected OS: Windows
Platform: Windows-11-10.0.26200-SP0
Python version: 3.13.7 (main, Aug 18 2025, 19:16:27) [MSC v.1944 64 bit (AMD64)]
Torch can be imported
# Checking device availability (selected: gpu=False, mps=False)
# Checking backend (selected: transformers)
Transformers backend selected
# Checking NGEC functionality
NGEC can be imported
Device set to use cpu
Attribute model test works
Actor resolver test is not working, error message:
unsupported operand type(s) for +: 'WindowsPath' and 'str'

```

## Windows with GPU and transformers

Known issue; don't run yet

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

```
Detected OS: Windows
Platform: Windows-11-10.0.26200-SP0
Python version: 3.13.7 (main, Aug 18 2025, 19:16:27) [MSC v.1944 64 bit (AMD64)]
Torch can be imported
# Checking device availability (selected: gpu=True, mps=False)
# Checking backend (selected: transformers)
Transformers backend selected
# Checking NGEC functionality
NGEC can be imported
`torch_dtype` is deprecated! Use `dtype` instead!
Device set to use cuda:0
Attribute model test works
Actor resolver test is not working, error message:
unsupported operand type(s) for +: 'WindowsPath' and 'str'
```


## Windows with CPU and vllm

```powershell
uv init --python 3.13 
uv venv --seed
.venv\Scripts\Activate

# Task 1: this next line needs to be verified
uv add torch torchvision
# Test this works
uv run check_cpu.py

uv add git+https://github.com/ahalterman/NGEC-2025 --extra models --extra vllm

uv run main.py --backend vllm 
```

## Windows with GPU and vllm

```powershell
uv init --python 3.13 
uv venv --seed
.venv\Scripts\Activate

# Task 1: this next line needs to be verified
uv add torch torchvision
# Test this works
uv run check_gpu.py

uv add git+https://github.com/ahalterman/NGEC-2025 --extra models --extra vllm

uv run main.py --backend vllm 
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


## Linux with CPU and vllm


## macOS with CPU and transformers

Not sure there even is an option for macOS CPU

## macOS with CPU and mlx

Not sure there even is an option for macOS CPU


