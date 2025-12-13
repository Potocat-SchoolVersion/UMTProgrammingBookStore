
def get_encryption_key() -> bytes:
    """
    Load encryption key from data/.key.
    Generate it if it doesn't exist.
    """
    DATA_DIR.mkdir(exist_ok=True)

    if not KEY_FILE.exists():
        key = Fernet.generate_key()
        KEY_FILE.write_bytes(key)
        return key

    return KEY_FILE.read_bytes()



def encrypt(filename: str):
    """
    Encrypt a file inside data/ folder (in-place).
    """
    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(f"{filename} not found in data/")

    key = get_encryption_key()
    fernet = Fernet(key)

    plaintext = file_path.read_bytes()
    ciphertext = fernet.encrypt(plaintext)

    file_path.write_bytes(ciphertext)



def decrypt(filename: str):
    """
    Decrypt a file inside data/ folder (in-place).
    """
    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(f"{filename} not found in data/")

    key = get_encryption_key()
    fernet = Fernet(key)

    ciphertext = file_path.read_bytes()
    plaintext = fernet.decrypt(ciphertext)

    file_path.write_bytes(plaintext)

