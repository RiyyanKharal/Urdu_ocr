# utils/file_utils.py
from PIL import Image, UnidentifiedImageError
from pdf2image import convert_from_path
from io import BytesIO
import os
import tempfile

def load_file_as_pages(uploaded_file, poppler_path=None):
    """
    Load an uploaded file (PDF or image) into a list of PIL.Image objects (pages).

    Args:
        uploaded_file: File-like object from Streamlit's file uploader.
        poppler_path: Path to Poppler bin folder (only needed on Windows).

    Returns:
        List of PIL.Image objects, one per page.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, uploaded_file.name)

        # Save uploaded file temporarily
        with open(input_path, "wb") as f:
            f.write(uploaded_file.read())

        # --- If PDF ---
        if uploaded_file.name.lower().endswith(".pdf"):
            try:
                pages = convert_from_path(
                    input_path,
                    dpi=300,
                    poppler_path=poppler_path
                )
                return pages
            except Exception as e:
                raise RuntimeError(f"Failed to convert PDF to images: {e}")

        # --- If image ---
        try:
            pil_img = Image.open(BytesIO(uploaded_file.getvalue())).convert("RGB")
            return [pil_img]
        except UnidentifiedImageError:
            raise ValueError("Unsupported file format. Please upload a PDF or an image.")
