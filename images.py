import os
from telegram import Update
from telegram.ext import ContextTypes
from ocr_service import ocr_space_file
from messages import handle_text_message

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📸 Foto diterima. Memproses...")
    photo = update.message.photo[-1]
    file = await photo.get_file()
    os.makedirs("downloads", exist_ok=True)
    path = f"downloads/{file.file_unique_id}.jpg"
    await file.download_to_drive(custom_path=path)
    text = ocr_space_file(path)
    os.remove(path)
    if text:
        context.user_data["ocr_text"] = text
        await update.message.reply_text("📄 Struk dibaca. Ketik:\n- tambahkan ke pengeluaran\n- tambahkan ke pemasukan")
    else:
        await update.message.reply_text("⚠️ Gagal membaca teks dari foto.")
