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
    print(f"\n✅ Klucze zapisane jako:\n  🔐 {priv_name}\n  🔓 {pub_name}")

def list_keys(pattern, label):
    keys = glob.glob(pattern)
    if not keys:
        print(f"⚠️  Brak dostępnych kluczy {label}.")
        return None
    print(f"\n📁 Dostępne klucze {label}:")
    for i, key in enumerate(keys):
        print(f"{i + 1}. {key}")
    while True:
        choice = input(f"Wybierz numer klucza {label}: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(keys):
            return keys[int(choice) - 1]
        else:
            print("❗ Nieprawidłowy wybór. Spróbuj ponownie.")

def sign_file():
    file_path = input("📄 Podaj ścieżkę do pliku do podpisania: ").strip()
    priv_path = list_keys("private_*.pem", "prywatnego")
    if not priv_path:
        return
    sig_path = file_path + ".sig"

    try:
        with open(priv_path, "rb") as f:
            priv_key = f.read()
        sign_file_and_save_signature(priv_key, file_path, sig_path)
        print(f"✅ Podpis zapisany jako: {sig_path}")
    except FileNotFoundError:
        print("❌ Nie znaleziono pliku klucza prywatnego.")

def verify_signature():
    file_path = input("📄 Podaj ścieżkę do oryginalnego pliku: ").strip()
    sig_path = input("📝 Podaj ścieżkę do pliku z podpisem (np. dokument.pdf.sig): ").strip()

    pub_key_path = list_keys("public_*.pem", "publicznego")
    if not pub_key_path:
        return

    try:
        with open(pub_key_path, "rb") as f:
            pub_key = f.read()
        result = verify_signature_from_file(pub_key, file_path, sig_path)
        if result:
            print("✅ Podpis jest prawidłowy.")
        else:
            print("❌ Podpis NIE jest prawidłowy.")
    except FileNotFoundError:
        print("❌ Nie znaleziono jednego z plików.")

def main():
    while True:
        print("\n=== MENU ===")
        print("1) Wygeneruj klucze")
        print("2) Podpisz plik")
        print("3) Zweryfikuj podpis")
        print("4) Wyjście")
        choice = input("Wybierz opcję (1/2/3/4): ").strip()

        if choice == "1":
            generate_keys()
        elif choice == "2":
            sign_file()
        elif choice == "3":
            verify_signature()
        elif choice == "4":
            print("👋 Zakończono program.")
            break
        else:
            print("❗ Nieprawidłowa opcja. Spróbuj ponownie.")

if __name__ == "__main__":
    main()