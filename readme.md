# 🧾 Telegram Syitter Bot

This Telegram bot helps you automatically log financial transactions into Google Sheets by sending:

* 🧾 Photos of receipts (JPG/PNG)
* 📄 PDF files
* 💬 Manual chat input (e.g., pengeluaran 5000 beli pulsa)

Supported by:

* Gemini 2.0 Flash (Google AI)
* Google Sheets API
* OCR.Space API (for image/PDF text extraction)

—

📁 Project Structure

Everything is stored in a flat directory (no subfolders):


—

🚀 Setup Guide

1. Create a Telegram Bot

* Open Telegram and search @BotFather
* Send /newbot → follow prompts
* Copy your bot token

2. Create a Google Sheet

* Create a new spreadsheet

* Add columns in Row 1:

  \| Timestamp | No | Tanggal | Nama Barang | Quantity | UoM | Keterangan | Harga | Pengeluaran | Pemasukan |

* Copy the spreadsheet ID from the URL:
  [https://docs.google.com/spreadsheets/d/SPREADSHEET\_ID/edit](https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit)

3. Create a Google Service Account

* Go to [https://console.cloud.google.com](https://console.cloud.google.com)
* Create a project → enable Google Sheets API
* Create a service account and download JSON key
* Share the spreadsheet with client\_email from that JSON (Editor access)

4. Get Gemini API Key

* Go to: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
* Generate an API key for Gemini Flash
* Paste it into your .env file (see below)

5. Get OCR API Key

* Go to: [https://ocr.space/OCRAPI](https://ocr.space/OCRAPI)
* Sign up and get your free API key

—

🔐 .env File Example

Create a .env file in the root directory and add:

```env
TELEGRAM_BOT_TOKEN=your_telegram_token
GEMINI_API_KEY=your_gemini_api_key
OCR_API_KEY=your_ocr_api_key
GOOGLE_CREDS_B64=your_base64_encoded_google_json
GOOGLE_SHEET_ID=your_google_sheet_id
GOOGLE_SHEET_NAME=Sheet1
```

To generate GOOGLE\_CREDS\_B64 from credentials.json:

For PowerShell:

```powershell
[Convert]::ToBase64String([System.IO.File]::ReadAllBytes("credentials.json"))
```

—

⚙️ Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the bot:

```bash
python bot.py
```

—

💬 Usage Examples

1. Manual chat input:

```
pengeluaran 20000 beli pulsa
pemasukan 100000 gaji harian
```

2. Send a receipt:

* Send a JPG or PDF
* Bot will OCR it and reply: "Type: tambahkan ke pengeluaran"

—

🧠 Features

* Detects and parses receipt text using OCR
* Automatically converts “UoM: x” to “pcs”
* Logs to Google Sheets (No & Timestamp auto-generated)
* Chat-style logging supported
* Supports both pemasukan (income) and pengeluaran (expense)
* Currency formatting ready for IDR (Rp)

—

📋 Google Sheets Format

Your spreadsheet should begin like this:

\| Timestamp | No | Tanggal | Nama Barang | Quantity | UoM | Keterangan | Harga | Pengeluaran | Pemasukan |

Begin input from Row 2. Format currency columns using Format → Number → Currency (Rp).

—

❓ FAQ

Q: Can I use this bot offline?
A: No. The bot needs access to Gemini and Google Sheets online.

Q: What Gemini model is used?
A: models/gemini-2.0-flash-latest (Fast and lightweight)

Q: Can I send a receipt photo from my phone?
A: Yes, just send a picture to the bot via Telegram.

—

📌 Notes

* You can run this bot on your local machine or a cloud server
* All logs print to terminal using Python logging

—

🛠 Built with Python, Google AI, and a dash of automation.
Feel free to fork, improve, and use it for your personal finance logging.

—
