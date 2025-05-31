import base64
import os
import tempfile

_temp_cred_path = None

def decode_and_save_google_credentials():
    global _temp_cred_path
    if _temp_cred_path:
        return _temp_cred_path
    encoded = os.getenv("GOOGLE_CREDS_B64")
    decoded = base64.b64decode(encoded)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="wb") as f:
        f.write(decoded)
        _temp_cred_path = f.name
    return _temp_cred_path
