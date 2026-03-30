import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_batch_text(combined_ocr_text):
    """Analyze 10 samples together for consolidated analysis"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an intelligent handwriting assistant. Analyze the collective content, correct OCR errors, and provide a summary."},
                {"role": "user", "content": combined_ocr_text}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"LLM Error: {str(e)}"
