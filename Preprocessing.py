import cv2
import numpy as np

def preprocess_image(image_bytes):
    """Preprocess handwriting image using OpenCV"""
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("Invalid image format")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)
    _, thresh = cv2.threshold(denoised, 150, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((2, 2), np.uint8)
    cleaned = cv2.morphologyOps(thresh, cv2.MORPH_CLOSE, kernel)

    return cleaned
