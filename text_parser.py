import json
import re
from logger import logger

def format_telegram_message_for_markdownv2(text: str) -> str:
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return "".join(['\\' + c if c in escape_chars else c for c in text])

def parse_ai_response_for_sheet_data(ai_response_text: str, timestamp: str):
    try:
        match = re.search(r"```json\s*([\s\S]+?)\s*```", ai_response_text)
        if not match:
            logger.warning("⚠️ Tidak ditemukan blok JSON dalam respons AI.")
            return []
        parsed_json = json.loads(match.group(1))
        rows = []
        nomor = 1
        for item in parsed_json:
            uom_raw = (item.get("UoM", "") or "").strip()
            uom = "pcs" if uom_raw.lower() == "x" else uom_raw
            row = [
                timestamp, str(nomor), item.get("Tanggal", ""), item.get("NamaBarang", ""),
                item.get("Quantity", ""), uom, item.get("Keterangan", ""), item.get("Harga", "0"),
                item.get("Pengeluaran", "0"), item.get("Pemasukan", "0")
            ]
            rows.append(row)
            nomor += 1
        return rows
    except Exception as e:
        logger.error("❌ Gagal parsing JSON dari AI.", exc_info=True)
        return []
