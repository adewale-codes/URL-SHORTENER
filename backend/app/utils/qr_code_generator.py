import qrcode
import os

QR_CODE_DIR = "qr_codes"  

def save_qr_code(short_url: str) -> str:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(short_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    os.makedirs(QR_CODE_DIR, exist_ok=True)

    img_path = os.path.join(QR_CODE_DIR, f"{short_url}.png")
    img.save(img_path)
    
    return img_path
