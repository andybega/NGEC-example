def gpu_available() -> bool:
    import torch
    if torch.cuda.is_available():
        gpu_device = torch.device("cuda")
        x = torch.ones(1, device=gpu_device)
        return True
    else:
        return False


if __name__ == "__main__":
    if gpu_available():
        print("Torch GPU is working.")
    else:
        print("Torch GPU is not working.")