import pdfplumber
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load model once
MODEL_NAME = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def ask_openai(prompt):
    try:
        inputs = tokenizer(prompt[:1000], return_tensors="pt", truncation=True)

        output_ids = model.generate(
            **inputs,
            max_new_tokens=150
        )

        result = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return result

    except Exception as e:
        return f"Local HF Error: {str(e)}"
