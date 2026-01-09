def mps_available() -> bool:
    import torch
    if torch.backends.mps.is_available():
        mps_device = torch.device("mps")
        x = torch.ones(1, device=mps_device)
        return True
    else:
        return False
    

if __name__ == "__main__":
    if mps_available():
        print("Torch MPS is working.")
    else:
        print("Torch MPS is not working.")