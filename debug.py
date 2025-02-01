def debug_environment():
    import sys
    import torch
    import platform
    import easyocr
    import cv2
    import numpy as np
    
    print("=== Environment Information ===")
    print(f"Python: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"PyTorch: {torch.__version__}")
    print(f"EasyOCR: {easyocr.__version__}")
    print(f"OpenCV: {cv2.__version__}")
    print(f"NumPy: {np.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    print(f"PyTorch architecture flags: {torch.__config__.show()}")
    
    # 檢查 OpenCC 版本
    try:
        import opencc
        print(f"OpenCC version: {opencc.__version__}")
    except Exception as e:
        print(f"OpenCC import error: {e}")
