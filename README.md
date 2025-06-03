# **Requirements**

    Python 3.8 or higher

# **Install dependencies**
    pip install pycryptodome

# **How to Use**

## **After running the script, a menu will appear:**

**1. Generate Keys**

    Choose option 1.

    The program will generate an RSA key pair and save them as:

        private_YYYYMMDD_HHMMSS.pem

        public_YYYYMMDD_HHMMSS.pem

**2. Sign a File**

    Choose option 2.

    Enter the path to the file you want to sign (e.g., document.pdf).

    Select a private key from the list.

    The program will create a signature file:

        document.pdf.sig

**3. Verify a Signature**
```
    Choose option 3.

    Enter the path to the original file (e.g., document.pdf).

    Enter the path to the signature file (e.g., document.pdf.sig).

    Select a public key from the list.

    The program will display whether the signature is valid or invalid.
```
# Output Example

```
private_20250604_101530.pem - private RSA key

public_20250604_101530.pem - public RSA key

document.pdf.sig - Signed document
```

# Notes

    Make sure to keep your private key secure.

    The public key can be shared freely for signature verification.
