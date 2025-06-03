from Crypto.PublicKey import RSA
from trng import ChaosTRNG

def generate_rsa_keys(bits=2048, image_folder="images"):
    trng = ChaosTRNG(image_folder=image_folder)
    print("🔧 Generowanie kluczy RSA...")
    key = RSA.generate(bits, randfunc=trng.randbytes)
    return key.export_key(), key.publickey().export_key()
