import os 
import json 
from transformers import pipeline
from ocr_test import extract_text_from_pdf

print("Loading NER pipeline...")
MODEL_PATH = "./my_ner_model"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Please ensure the model is trained and saved correctly.")
    exit()

new_pipline = pipeline(
    "ner",
    model=MODEL_PATH,
    tokenizer=MODEL_PATH,
    aggregation_strategy="simple"
)

print("NER pipeline loaded successfully.")

def extract_entities_from_text(file_path):
    print("Step 1: Running OCR on the document...")
    raw_text = extract_text_from_pdf(file_path)

    print("\n" + "="*20 + " OCR OUTPUT " + "="*20)
    print(raw_text)
    print("="*52 + "\n")

    if "Error" in raw_text or not raw_text.strip():
        print(f"OCR Failed")
        return {"error": raw_text}
    
    print("OCR completed successfully.")

    print("Step 2: Running NER on the extracted text...")
    ner_results = new_pipline(raw_text)
    if ner_results is None :
        print("NER failed or returned no results.")
        return {"error": "No entities found."}
    if not isinstance(ner_results, list):
        print("NER results are not in the expected list format.")
        return {"error": "Invalid NER results format."}
    
    print("NER completed successfully.")

    print("Step 3: Formatting NER results...")
    extracted_data = {}

    for entity in ner_results:
        if isinstance(entity, dict):
            entity_group = entity['entity_group']
            entity_value = entity['word'].strip()

            if entity_group in extracted_data:
                extracted_data[entity_group] += " " + entity_value
            else:
                extracted_data[entity_group] = entity_value
    
    return extracted_data

if __name__ == "__main__":
    test_file_name = "Detailed_Invoice.pdf" 
    test_file_path = "/home/alxmassy/dev/documintAI/Detailed_Invoice.pdf"

    if os.path.exists(test_file_path):
        print("-"*50)
        print(f"Processing file: {test_file_path}")
        print("-"*50)

        final_data = extract_entities_from_text(test_file_path)

        print("\n--- Final Extracted Entities ---")
        print(json.dumps(final_data, indent=2))
        print("-"*50)
    else:
        print(f"File {test_file_path} does not exist. Please check the file path and try again.")