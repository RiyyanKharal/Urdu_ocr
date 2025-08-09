# app.py
import streamlit as st
from core.ocr import ocr_image
from core.preprocessing import clean_urdu_text
from core.metrics import compute_metrics
from utils.file_utils import load_file_as_pages

# -------------------------------
# Streamlit Page Config
# -------------------------------
st.set_page_config(
    page_title="Urdu OCR Dashboard",
    layout="wide"
)
st.title("📜 Urdu OCR — Image/PDF → Unicode Text + Accuracy Dashboard")

st.markdown("""
Upload Urdu text images or PDFs, run OCR, clean the text, and measure accuracy against reference text.
""")

# -------------------------------
# Sidebar Settings
# -------------------------------
st.sidebar.header("⚙️ OCR Settings")

lang = st.sidebar.text_input("OCR Language (Tesseract code)", value="urd")
do_denoise = st.sidebar.checkbox("Denoise", value=True)
do_threshold = st.sidebar.checkbox("Threshold", value=True)
do_deskew = st.sidebar.checkbox("Deskew", value=False)
poppler_path = st.sidebar.text_input(
    "Poppler Path (Windows only)",
    value="",
    help="Path to poppler bin folder if running on Windows."
)

# -------------------------------
# File Upload
# -------------------------------
uploaded_files = st.file_uploader(
    "Upload Image(s) or PDF(s)",
    type=["png", "jpg", "jpeg", "tif", "tiff", "pdf"],
    accept_multiple_files=True
)

references = []
clean_texts = []

if uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) uploaded.")

    # Optional reference text file for accuracy
    ref_texts_uploaded = st.file_uploader(
        "Upload Reference Text Files (in order, optional)",
        type=["txt"],
        accept_multiple_files=True
    )

    if ref_texts_uploaded:
        for ref_file in ref_texts_uploaded:
            references.append(ref_file.read().decode("utf-8").strip())

    # Process each file
    for idx, uf in enumerate(uploaded_files):
        st.subheader(f"📄 File {idx+1}: {uf.name}")
        pages = load_file_as_pages(uf, poppler_path if poppler_path else None)

        for p_idx, page_img in enumerate(pages):
            st.write(f"**Page {p_idx+1}**")

            # Run OCR
            raw_text = ocr_image(
                page_img,
                lang=lang,
                do_denoise=do_denoise,
                do_threshold=do_threshold,
                do_deskew=do_deskew
            )

            # Clean Urdu text
            cleaned_text = clean_urdu_text(raw_text)
            clean_texts.append(cleaned_text)

            # Display results
            col1, col2 = st.columns(2)
            with col1:
                st.image(page_img, caption=f"Page {p_idx+1} Image", use_container_width=True)
            with col2:
                st.text_area(
                    f"OCR Output (Cleaned, Page {p_idx+1})",
                    cleaned_text,
                    height=200
                )

            # If reference exists, show
            if p_idx < len(references):
                st.text_area(
                    f"Reference Text (Page {p_idx+1})",
                    references[p_idx],
                    height=200
                )

    # -------------------------------
    # Metrics Computation
    # -------------------------------
    if references and len(references) == len(clean_texts):
        st.subheader("📊 Accuracy Metrics")
        per_page_metrics, overall_metrics = compute_metrics(clean_texts, references)

        st.markdown("**Per-Page Metrics:**")
        st.dataframe(per_page_metrics)

        st.markdown("**Overall Metrics:**")
        st.json(overall_metrics)
    elif references:
        st.warning("⚠️ Number of reference texts does not match number of pages.")
