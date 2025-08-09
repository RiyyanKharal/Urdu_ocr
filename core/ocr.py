# core/ocr.py
from PIL import Image
import pytesseract
import cv2
import numpy as np
import os

# --- Auto-configure Tesseract path for Windows ---
if os.name == "nt":  # Windows only
    tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    tessdata_path = r"C:\Program Files\Tesseract-OCR\tessdata"
    if os.path.exists(tesseract_path):
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        os.environ["TESSDATA_PREFIX"] = tessdata_path
    else:
        raise FileNotFoundError(
            f"Tesseract not found at {tesseract_path}. "
            "Install from https://github.com/UB-Mannheim/tesseract/wiki"
        )

def pil_to_np(pil_img):
    """
    Convert a PIL Image to a NumPy array (RGB).
    """
    pil_rgb = pil_img.convert("RGB")
    return np.array(pil_rgb)

def preprocess_image_cv(np_img, resize_max_dim=1800, do_denoise=True, do_threshold=True, do_deskew=False):
    """
    Preprocess an image for OCR:
    - Resize if too large
    - Denoise (optional)
    - Threshold (optional)
    - Deskew (optional)
    Returns: Grayscale/thresholded NumPy array
    """
    if np_img.shape[2] == 3:
        img = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)
    else:
        img = np_img.copy()

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Resize if larger than max dimension
    h, w = gray.shape[:2]
    max_dim = max(h, w)
    if max_dim > resize_max_dim:
        scale = resize_max_dim / float(max_dim)
        gray = cv2.resize(gray, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)

    # Apply bilateral denoising if enabled
    if do_denoise:
        gray = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)

    # Apply Otsu thresholding if enabled
    if do_threshold:
        _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        gray = th

    # Deskew if enabled
    if do_deskew:
        coords = np.column_stack(np.where(gray > 0))
        if coords.size != 0:
            angle = cv2.minAreaRect(coords)[-1]
            if angle < -45:
                angle = -(90 + angle)
            else:
                angle = -angle
            (h, w) = gray.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            gray = cv2.warpAffine(
                gray, M, (w, h),
                flags=cv2.INTER_CUBIC,
                borderMode=cv2.BORDER_REPLICATE
            )

    return gray

def ocr_image(pil_img, lang="urd", do_denoise=True, do_threshold=True, do_deskew=False):
    """
    Run OCR on a PIL image using Tesseract with optional preprocessing.
    """
    np_img = pil_to_np(pil_img)
    pre = preprocess_image_cv(
        np_img,
        do_denoise=do_denoise,
        do_threshold=do_threshold,
        do_deskew=do_deskew
    )
    pil_pre = Image.fromarray(pre)
    config = '--oem 3 --psm 4'
    return pytesseract.image_to_string(pil_pre, lang=lang, config=config)
