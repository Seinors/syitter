import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def call_gemini_agent(prompt: str) -> str:
    model = genai.GenerativeModel(
        model_name="models/gemini-2.0-flash-001",
        generation_config={"temperature": 0.7}
    )
    response = model.generate_content(prompt)
    return response.text
