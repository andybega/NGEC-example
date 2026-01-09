
import argparse
import platform


def detect_platform() -> str:
    return platform.platform()


def get_es_credentials() -> tuple[str, str]:
    import os
    user, password = os.getenv("ES_USER"), os.getenv("ES_PASSWORD")
    if user is None or password is None:
        raise ValueError("ES_USER and ES_PASSWORD environment variables must be set")
    return user, password


def torch_available() -> bool:
    try:
        import torch
        return True
    except ImportError:
        return False


def mps_available() -> bool:
    import torch
    if torch.backends.mps.is_available():
        mps_device = torch.device("mps")
        x = torch.ones(1, device=mps_device)
        return True
    else:
        return False


def gpu_available() -> bool:
    import torch
    if torch.cuda.is_available():
        gpu_device = torch.device("cuda")
        x = torch.ones(1, device=gpu_device)
        return True
    else:
        return False


def vllm_importable() -> bool:
    try:
        import vllm  # noqa: F401
        return True
    except ImportError:
        return False


def mlx_importable() -> bool:
    try:
        import mlx  # noqa: F401
        return True
    except ImportError:
        return False


def ngec_importable() -> bool:
    try:
        import ngec
        return True
    except ImportError:
        return False


def attribute_model_works(gpu: bool, backend: str) -> tuple[bool, str]:
    try:
        import logging

        from ngec.attribute_model import AttributeModel, AttributeModelInput
        from ngec.logging import setup_logging
    
        setup_logging()
        logging.getLogger("ngec.attribute_model").setLevel(logging.WARNING)

        am = AttributeModel(silent=True, gpu=gpu, backend=backend)

        input = [
            AttributeModelInput(
                event_text="A group of Hindu nationalists rioted in Dehli last week, burning Muslim shops.",
                event_type="PROTEST"
            )
        ]

        _ = am.process(input)

        return True, ""
    
    except Exception as e:
        return False, str(e)


def actor_resolver_works(user, password) -> tuple[bool, str]:
    try:
        import logging


        from ngec import ActorResolver
        from ngec.es_client import setup_es_client
        from ngec.logging import setup_logging

        setup_logging()
        logging.getLogger("ngec.actor_resolution").setLevel(logging.WARNING)
        logging.getLogger("ngec.wiki_matcher").setLevel(logging.WARNING)
        logging.getLogger("tzlocal").setLevel(logging.WARNING)
        logging.getLogger("sentence_transformers.SentenceTransformer").setLevel(logging.WARNING)

        client = setup_es_client(hosts=["localhost"], port=9200, user=user, password=password)

        resolver = ActorResolver(es_client=client)
        resolver.actor_to_code("Angela Merkel")

        return True, ""
    
    except Exception as e:
        return False, str(e)




def main(os="macOS", gpu=False, mps=True, backend="transformers"):
    import sys

    print(f"Platform: {detect_platform()}")
    print(f"Python version: {sys.version}")


    user, password = get_es_credentials()

    if not torch_available():
        print("Torch cannot be imported, skipping rest")
        return 
    else:
        print("Torch can be imported")

    # Check for CPU/GPU/MPS availability
    print(f"# Checking device availability (selected: gpu={gpu}, mps={mps})")
    
    if os=="macOS": 
        if mps:
            if mps_available():
                print("MPS is available")
            else:
                print("MPS is not available, skipping rest")
                return
        else:
            print("Using CPU")
    
    if os=="linux" or os=="windows":
        print("Not implemented yet")


    # Check for backend availability
    print(f"# Checking backend (selected: {backend})")
    
    if backend=="vllm":
        if not vllm_importable():
            print("vLLM backend selected but vLLM cannot be imported, skipping rest")
            return
        else:
            print("vLLM backend selected and vLLM can be imported")
    
    if backend=="mlx":
        if not mlx_importable():
            print("MLX backend selected but MLX cannot be imported, skipping rest")
            return
        else:
            print("MLX backend selected and MLX can be imported")
    
    if backend=="transformers":
        print("Transformers backend selected")



    # Substantive tests using NGEC
    print("# Checking NGEC functionality")

    if not ngec_importable():
        print("NGEC cannot be imported")
        return
    else:
        print("NGEC can be imported")
    
    works, error = attribute_model_works(gpu=gpu, backend=backend)
    if not works:
        print("Attribute model test is not working, error message:")
        print(error)
    else:
        print("Attribute model test works")


    works, error = actor_resolver_works(user, password)
    if not works:
        print("Actor resolver test is not working, error message:")
        print(error)
    else:
        print("Actor resolver test works")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test NGEC installation")
    parser.add_argument(
        "--backend",
        choices=["transformers", "vllm", "mlx"],
        default="transformers",
        help="Backend to use (default: transformers)"
    )
    parser.add_argument(
        "--gpu",
        action="store_true",
        help="Enable GPU"
    )
    parser.add_argument(
        "--mps",
        action="store_true",
        help="Enable MPS"
    )
    
    args = parser.parse_args()
    
    gpu = args.gpu
    mps = args.mps

    # Detect platform
    system = platform.system()
    os_map = {"Darwin": "macOS", "Windows": "Windows", "Linux": "Linux"}
    detected_os = os_map.get(system, "Linux")

    print(f"Detected OS: {detected_os}")
    
    main(os=detected_os, gpu=gpu, mps=mps, backend=args.backend)
