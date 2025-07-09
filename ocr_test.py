import os
import pytesseract
import fitz
import json
from PIL import Image

def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"The file {pdf_path} does not exist.")
    
    file_extension = os.path.splitext(pdf_path)[1].lower()
    extracted_text = ""

    if file_extension == '.pdf':
        try:
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                mat = fitz.Matrix(300/72, 300/72)  # 300 DPI scaling
                pix = page.get_pixmap(matrix=mat)
                img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
                extracted_text += pytesseract.image_to_string(img) + "\n\n"
            doc.close()
        except Exception as e:
            raise RuntimeError(f"An error occurred while processing the PDF: {e}")
    elif file_extension in ['.jpg', '.jpeg', '.png']:
        try:
            img = Image.open(pdf_path)
            extracted_text = pytesseract.image_to_string(img)
        except Exception as e:
            raise RuntimeError(f"An error occurred while processing the image: {e}")
    else:
        raise ValueError("Unsupported file format. Please provide a PDF file.")
    return extracted_text

# if __name__ == "__main__":
#     sample_file = os.path.join('data', 'invoice_01.pdf')

#     print(f"Extracting text from {sample_file}...")
#     raw_text = extract_text_from_pdf(sample_file)
#     print(raw_text)

#     output_dir = "raw_text_for_annotation"
#     os.makedirs(output_dir, exist_ok=True)

#     for filename in os.listdir('data'):
#         file_path = os.path.join('data', filename)
#         if os.path.isfile(file_path):
#             print(f"Extracting text from {file_path}...")
#             text = extract_text_from_pdf(file_path)
#             output_filename = os.path.splitext(filename)[0] + '_extracted.txt'
#             with open(os.path.join(output_dir, output_filename), 'w', encoding="utf-8") as f:
#                 f.write(text)
#             print(f"Extracted text saved to {output_filename}")


if __name__ == "__main__":
    DATA_DIR = "data"
    OUTPUT_JSON_FILE = "ocr_output_for_label_studio.json"

    # This list will hold one dictionary for each document
    tasks_for_label_studio = []

    if not os.path.exists(DATA_DIR):
        print(f"Error: Data directory '{DATA_DIR}' not found. Please create it and add your documents.")
    else:
        # Loop through every file in the 'data' directory
        for filename in os.listdir(DATA_DIR):
            file_path = os.path.join(DATA_DIR, filename)
            if os.path.isfile(file_path):
                print(f"Processing: {filename}...")

                # Get the raw text from the document
                raw_text = extract_text_from_pdf(file_path)

                # Skip if there was an error
                if "Error:" in raw_text:
                    print(f"  -> Skipped due to error: {raw_text}")
                    continue

                # Create the JSON structure that Label Studio expects for each task
                # The key 'text' must match the <Text name="text" ...> tag in the Labeling Interface
                task = {
                    "data": {
                        "text": raw_text
                    }
                }
                tasks_for_label_studio.append(task)
                print(f"  -> Added to task list.")

        # Write the entire list of tasks to a single JSON file
        with open(OUTPUT_JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks_for_label_studio, f, indent=2)

        print(f"\nSuccessfully created '{OUTPUT_JSON_FILE}' with {len(tasks_for_label_studio)} tasks.")
        print("You can now import this file into Label Studio.")