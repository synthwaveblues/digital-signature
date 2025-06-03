**Requirements**
● Python 3.8+
● Installed libraries: pip install pycryptodome

**How to use?**
After launching the program, a menu will appear:

**1. Generate keys**
● Select option 1.
● The program will create an RSA key pair and save them as
private_YYYYMMDD_HHMMSS.pem and
public_YYYYMMDD_HHMMSS.pem.
**
2. Sign a file**
● Select option 2.
● Enter the path to the file you want to sign (e.g., document.pdf).
● Select a private key from the list.
● The program will create a signature and save it as document.pdf.sig.
**
3. Verify signature**
● Select option 3.
● Enter the path to the original file (e.g., document.pdf).
● Enter the path to the signature (e.g., document.pdf.sig).
● Select a public key from the list.
● The program will inform you whether the signature is valid.
