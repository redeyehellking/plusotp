import qrcode
from io import BytesIO

def generate_qr_code(upi_id, amount):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f"upi://pay?pa={upi_id}&am={amount}")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    bio = BytesIO()
    img.save(bio, "PNG")
    bio.seek(0)
    return bio
