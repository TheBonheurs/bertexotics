import uuid
import qrcode

# Generate and insert unique product codes, and create corresponding QR codes
num_codes = 10  # Number of codes to generate
base_url = "http://127.0.0.1:5000/verify?code="

codes = {str(uuid.uuid4()) for _ in range(num_codes)}

for code in codes:
    qr = qrcode.make(base_url + code)
    qr.save(f"qrcodes/{code}.png")

print(f'Created {num_codes} unique product codes and QR codes.')
