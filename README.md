Urdu Text Recognition from Images and PDFs
📜 Urdu OCR — Image/PDF → Unicode Text + Accuracy Dashboard

Upload Urdu text images or PDFs, run OCR with preprocessing, clean the extracted text, and measure accuracy against reference text files.

Features
Supports image files (PNG, JPG, JPEG, TIFF) and multi-page PDFs

Preprocessing pipeline with denoising, thresholding, resizing, and deskewing options

OCR using Tesseract with Urdu language support

Text cleaning and normalization for Urdu script

Accuracy evaluation with Character Error Rate (CER) and Word Error Rate (WER)

Interactive dashboard UI built with Streamlit and optionally deployable with Gradio

Setup and Run Instructions
1. Prerequisites
Python 3.8 or higher installed

Tesseract OCR installed and added to your system PATH

For Windows, ensure tesseract.exe path is configured in the app or environment variables

Poppler installed (required for PDF to image conversion)

Windows users: Download binaries and set poppler_path in the app sidebar

2. Clone the Repository
bash
Copy
Edit
git clone https://github.com/RiyyanKharal/Urdu_ocr.git
cd urdu_ocr_dashboard
3. Install Python Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Run the Application
bash
Copy
Edit
streamlit run app.py
This will launch the web dashboard locally at http://localhost:8501.

Usage
Upload one or more Urdu text images or PDF files.

Optionally upload corresponding reference text files (UTF-8 encoded .txt) for accuracy measurement.

Configure OCR preprocessing options in the sidebar.

View OCR output and accuracy metrics per page.



Acknowledgments
Tesseract OCR for text recognition

OpenCV and Pillow for image preprocessing

Streamlit and Gradio for web UI frameworks

