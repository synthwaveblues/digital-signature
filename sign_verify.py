from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from key_generator import generate_rsa_keys
import os

def sign_file_and_save_signature(private_key_pem: bytes, file_path: str, signature_path: str):
    key = RSA.import_key(private_key_pem)
    with open(file_path, 'rb') as f:
        file_data = f.read()
    h = SHA256.new(file_data)
    signature = pkcs1_15.new(key).sign(h)
    with open(signature_path, 'wb') as f:
        f.write(signature)
    print(f"✅ Podpis zapisany do: {signature_path}")

def verify_signature_from_file(public_key_pem: bytes, file_path: str, signature_path: str) -> bool:
    key = RSA.import_key(public_key_pem)
    with open(file_path, 'rb') as f:
        file_data = f.read()
    with open(signature_path, 'rb') as f:
        signature = f.read()
    h = SHA256.new(file_data)
    try:
        pkcs1_15.new(key).verify(h, signature)
        print("✅ Podpis jest prawidłowy.")
        return True
    except (ValueError, TypeError):
        print("❌ Podpis nieprawidłowy!")
        return False

if __name__ == "__main__":
    priv_key, pub_key = generate_rsa_keys()

    file_path = "dokument.pdf"
    signature_path = file_path + ".sig"

    sign_file_and_save_signature(priv_key, file_path, signature_path)
    verify_signature_from_file(pub_key, file_path, signature_path)
