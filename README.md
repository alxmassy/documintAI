# DocuMint AI

DocuMint AI is a full-stack web application designed to automate financial document processing. Users can upload invoices, receipts, or other financial documents (PDFs/Images), and the system will use Optical Character Recognition (OCR) and a custom-trained Natural Language Processing (NLP) model to extract key information.

The extracted data is presented on a clean dashboard, enabling users to quickly view and manage important financial details and export them for further use.

<!-- TODO: Add a screenshot of your app's dashboard -->
<!-- ![FinDoc-Extractor Dashboard](path/to/screenshot.png) -->

---

## ✨ Key Features
*   **Intelligent Data Extraction**: A powerful backend pipeline that:
    1.  Converts documents to text using **OCR (Tesseract)**.
    2.  Identifies key entities using a **custom-trained NER model (Hugging Face Transformers)**.
*   **Key Entities Extracted**:
    *   Company Name
    *   Invoice Number
    *   Total Amount
    *   Due Date
    *   Account Number
*   **Data Export**: Export extracted data to CSV for easy integration with other tools.

---

## 🛠️ Tech Stack

*   **Backend**: **Python** with **FastAPI**
*   **Machine Learning**: **Hugging Face Transformers** (for custom NER model), **PyTesseract** (for OCR)
*   **Database**: **PostgreSQL**
