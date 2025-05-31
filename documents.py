import os
from telegram import Update
from telegram.ext import ContextTypes
from ocr_service import ocr_space_file
from messages import handle_text_message

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    if doc.mime_type != 'application/pdf':
        await update.message.reply_text("❌ Maaf, hanya file PDF yang didukung.")
        return
    await update.message.reply_text("📥 File diterima. Memproses...")
    file = await doc.get_file()
    os.makedirs("downloads", exist_ok=True)
    path = f"downloads/{doc.file_unique_id}.pdf"
    await file.download_to_drive(custom_path=path)
    text = ocr_space_file(path)
    os.remove(path)
    if text:
        context.user_data["ocr_text"] = text
        await update.message.reply_text("📄 Struk dibaca. Ketik:\n- tambahkan ke pengeluaran\n- tambahkan ke pemasukan")
    else:
        await update.message.reply_text("⚠️ Gagal membaca teks dari file.")
