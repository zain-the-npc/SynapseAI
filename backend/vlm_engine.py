from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image
import torch

# Load a tiny, fast model
model_id = "vikhyatk/moondream2"
revision = "2024-08-05" # or latest

model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True, revision=revision)
tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)

def describe_note(image_path):
    image = Image.open(image_path)
    enc_image = model.encode_image(image)
    # This prompt tells the VLM to be a study assistant
    prompt = "Transcribe the handwriting in this image and describe any diagrams or formulas in detail for a study guide."
    description = model.answer_question(enc_image, prompt, tokenizer)
    return description