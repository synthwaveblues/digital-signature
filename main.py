import glob
import datetime
from key_generator import generate_rsa_keys
from sign_verify import sign_file_and_save_signature, verify_signature_from_file

def generate_keys():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    priv_name = f"private_{timestamp}.pem"
    pub_name = f"public_{timestamp}.pem"
    priv_key, pub_key = generate_rsa_keys()
    with open(priv_name, "wb") as f:
        f.write(priv_key)
    with open(pub_name, "wb") as f:
        f.write(pub_key)
    print(f"\nKeys saved as:\n  {priv_name}\n  {pub_name}")

def list_keys(pattern, label):
    keys = glob.glob(pattern)
    if not keys:
        print(f"No available {label} keys.")
        return None
    print(f"\nAvailable {label} keys:")
    for i, key in enumerate(keys):
        print(f"{i + 1}. {key}")
    while True:
        choice = input(f"Select the {label} key number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(keys):
            return keys[int(choice) - 1]
        else:
            print("Invalid selection. Try again.")

def sign_file():
    file_path = input("Enter the path to the file to sign: ").strip()
    priv_path = list_keys("private_*.pem", "private")
    if not priv_path:
        return
    sig_path = file_path + ".sig"

    try:
        with open(priv_path, "rb") as f:
            priv_key = f.read()
        sign_file_and_save_signature(priv_key, file_path, sig_path)
        print(f"Signature saved as: {sig_path}")
    except FileNotFoundError:
        print("Private key file not found.")

def verify_signature():
    file_path = input("Enter the path to the original file: ").strip()
    sig_path = input("Enter the path to the signature file (e.g., document.pdf.sig): ").strip()

    pub_key_path = list_keys("public_*.pem", "public")
    if not pub_key_path:
        return

    try:
        with open(pub_key_path, "rb") as f:
            pub_key = f.read()
        result = verify_signature_from_file(pub_key, file_path, sig_path)
        if result:
            print("Signature is valid.")
        else:
            print("Signature is NOT valid.")
    except FileNotFoundError:
        print("One of the files was not found.")

def main():
    while True:
        print("\n=== MENU ===")
        print("1) Generate keys")
        print("2) Sign file")
        print("3) Verify signature")
        print("4) Exit")
        choice = input("Choose an option (1/2/3/4): ").strip()

        if choice == "1":
            generate_keys()
        elif choice == "2":
            sign_file()
        elif choice == "3":
            verify_signature()
        elif choice == "4":
            print("Program terminated.")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
