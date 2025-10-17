
import torch

def mps_available() -> bool:
    try:
        return torch.backends.mps.is_available()
    except AttributeError:
        return False

def gpu_available() -> bool:
    return torch.cuda.is_available()


def vllm_importable() -> bool:
    try:
        import vllm  # noqa: F401
        return True
    except ImportError:
        return False