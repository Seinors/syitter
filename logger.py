import logging

# Buat logger utama
logger = logging.getLogger("telegram.bot")
logger.setLevel(logging.INFO)

# Tambahkan handler untuk console output
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
