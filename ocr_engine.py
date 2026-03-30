from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch
import numpy as np

processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')
model.eval()

def recognize_handwriting(image_array):
    """Recognize handwriting from preprocessed image using TrOCR"""
    try:
        if len(image_array.shape) == 2:
            image = Image.fromarray(image_array).convert("RGB")
        else:
            image = Image.fromarray(image_array)

        pixel_values = processor(images=image, return_tensors="pt").pixel_values

        with torch.no_grad():
            generated_ids = model.generate(pixel_values, max_length=512)

        generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        return generated_text.strip()

    except Exception as e:
        return f"OCR Error: {str(e)}"
