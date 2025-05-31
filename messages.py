from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
import re
from ai_agent import call_gemini_agent
from sheets import append_to_google_sheet
from text_parser import parse_ai_response_for_sheet_data, format_telegram_message_for_markdownv2

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE, override_text=None):
    text = override_text or update.message.text
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lower_text = text.lower().strip()

    # Perintah setelah OCR: tambahkan ke pengeluaran / pemasukan
    if lower_text in ["tambahkan ke pengeluaran", "tambahkan ke pemasukan"]:
        saved_ocr = context.user_data.get("ocr_text")
        if not saved_ocr:
            await update.message.reply_text("⚠️ Tidak ada data OCR tersimpan. Kirim struk terlebih dahulu.")
            return
        jenis = "pengeluaran" if "pengeluaran" in lower_text else "pemasukan"
        await update.message.reply_text(f"✅ Memproses OCR sebagai {jenis}...")
        await handle_text_message(update, context, override_text=saved_ocr + f"\nTambahkan ke {jenis}")
        context.user_data["ocr_text"] = None
        return

    # Input manual: pemasukan/pengeluaran 5000 beli pulsa
    match = re.match(r'(?i)(pengeluaran|pemasukan)\s+([\d.,]+)\s+(.*)', text)
    if match:
        jenis = match.group(1).lower()
        nominal = match.group(2).replace('.', '').replace(',', '')
        keterangan = match.group(3)
        row = [
            ts, "", datetime.now().strftime("%Y-%m-%d"), "", "", "",
            keterangan, nominal,
            nominal if jenis == "pengeluaran" else "0",
            nominal if jenis == "pemasukan" else "0"
        ]
        append_to_google_sheet([row])
        await update.message.reply_text(f"✅ {jenis.capitalize()} sebesar Rp {nominal} dicatat.")
        return

    # Proses AI dengan Gemini
    prompt = f"""
Kamu adalah asisten pencatat keuangan. Berdasarkan isi berikut:

{text}

Ekstrak data transaksi dan ubah menjadi array JSON dengan struktur berikut:

[
  {{
    "Tanggal": "2024-05-01",
    "NamaBarang": "Kabel USB",
    "Quantity": "2",
    "UoM": "pcs",
    "Keterangan": "Alfamart",
    "Harga": "10000",
    "Pengeluaran": "20000",
    "Pemasukan": "0"
  }}
]

Petunjuk:
- Semua nilai dalam bentuk string.
- Jika UoM adalah 'x', ubah ke 'pcs'.
- Jika transaksi pemasukan, isi kolom Pemasukan > 0 dan Pengeluaran = 0.
- Jika transaksi pengeluaran, isi kolom Pengeluaran > 0 dan Pemasukan = 0.
- Timestamp dan Nomor akan ditambahkan otomatis.
- Jangan tambahkan kolom 'Total'.
- Kirim hanya JSON.
"""

    response = call_gemini_agent(prompt)
    rows = parse_ai_response_for_sheet_data(response, ts)

    if rows:
        append_to_google_sheet(rows)

    summary = f"✅ Berhasil menambahkan {len(rows)} transaksi." if rows else "⚠️ Tidak ada data valid ditemukan."
    msg = format_telegram_message_for_markdownv2(summary)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='MarkdownV2')
