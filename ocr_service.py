import requests
from config import OCR_API_KEY

def ocr_space_file(filename):
    with open(filename, 'rb') as f:
        r = requests.post(
            'https://api.ocr.space/parse/image',
            files={'file': f},
            data={'apikey': OCR_API_KEY, 'language': 'eng', 'OCREngine': 2}
        )
    try:
        result = r.json()
        return result['ParsedResults'][0]['ParsedText']
    except Exception:
        return ""
