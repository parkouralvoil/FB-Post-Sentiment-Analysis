from cryptography.fernet import Fernet

def load_key():
    """Loads the secret key from a file"""
    with open("KEY.key", "rb") as key_file:
        return key_file.read()

key = load_key()
cipher = Fernet(key)

def encrypt_string(plain_text: str) -> str:
    """Encrypts a string
    
    Parameters
    ----------
    plain_text: str
        The text that you want to encrypt
    
    Returns
    -------
    str
        The cipher text
    """
    return cipher.encrypt(plain_text.encode()).decode()

def decrypt_string(encrypted_text: str) -> str:
    """Decrypts a string
    
    Parameters
    ----------
    encrypted_text: str
        The cipher text to be decrypted

    Returns
    -------
    str
        The decrypted plaintext
    """
    if encrypted_text:
        return cipher.decrypt(encrypted_text.encode()).decode()
    return ""

if __name__ == "__main__":
    text = "Nah I'd Win"
    text = encrypt_string(text)
    print(decrypt_string(text))

