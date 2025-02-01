def debug_environment():
    import sys
    import torch
    import platform
    import easyocr
    import cv2
    import numpy as np

    env_info = {
        "Python": sys.version,
        "Platform": platform.platform(),
        "PyTorch": torch.__version__,
        "EasyOCR": easyocr.__version__,
        "OpenCV": cv2.__version__,
        "NumPy": np.__version__,
        "CUDA available": torch.cuda.is_available(),
        "PyTorch architecture flags": torch.__config__.show(),
    }

    # 檢查 OpenCC 版本
    try:
        import opencc
        env_info["OpenCC"] = opencc.__version__
    except Exception as e:
        env_info["OpenCC"] = f"Import error: {e}"

    return env_info
