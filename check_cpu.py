
def torch_available() -> bool:
    try:
        import torch
        x = torch.ones(1)
        return True
    except ImportError:
        return False


if __name__=="__main__":
    if torch_available():
        print("Torch is working.")
    else:
        print("Torch is not working.")