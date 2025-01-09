from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import datetime


class AESCipher:
    """
    A class to perform AES encryption and decryption.

    Attributes:
        key (bytes): The secret key used for encryption and decryption.
        iv (bytes): The initialization vector used for encryption.
    """

    def __init__(self, key):
        """
        Initializes the AESCipher object.

        Args:
            key (str): The secret key used for encryption and decryption.
        """
        self.key = key.encode('utf-8')
        self.iv = get_random_bytes(16)

    def encrypt_string(self, plain_text):
        """
        Encrypts a given plaintext string.

        Args:
            plain_text (str): The plaintext string to be encrypted.

        Returns:
            str: The encrypted text.
        """
        cipher = AES.new(self.key, AES.MODE_CFB, iv=self.iv)
        encrypted_text = cipher.encrypt(
            pad(plain_text.encode('utf-8'), AES.block_size))
        return base64.b64encode(self.iv + encrypted_text).decode('utf-8')

    def decrypt_string(self, cipher_text):
        """
        Decrypts a given ciphertext string.

        Args:
            cipher_text (str): The ciphertext string to be decrypted.

        Returns:
            str: The decrypted text.
        """
        combined_data = base64.b64decode(cipher_text.encode('utf-8'))
        iv = combined_data[:16]
        encrypted_bytes = combined_data[16:]

        cipher = AES.new(self.key, AES.MODE_CFB, iv=iv)
        decrypted_text = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
        return decrypted_text.decode('utf-8')


def custom_api(db, models, data):
    """
    A custom API function for encryption and database operations.

    Args:
        db: The database connection object.
        models: The database models.
        data (dict): A dictionary containing 'created_by', 'publickey', and 'secret_key'.

    Returns:
        dict or str: A dictionary containing the encrypted secret key if successful, or a failure message.

    Example Usage:
        key = "1226193703425550"
        aes_cipher = AESCipher(key)
        x = datetime.datetime.now()
        text_to_encrypt = x.strftime("%Y%m%d%H%M%S")
        encrypted_text = aes_cipher.encrypt_string(text_to_encrypt)
        print(f"Encrypted Text: {encrypted_text}")

    Note:
        Uncomment the decryption part for decrypting the encrypted text.
    """
    data = {
        'created_by': data['created_by'],
        'publickey': data['publickey'],
        'secret_key': data['secret_key'],
    }

    key = data['secret_key']
    aes_cipher = AESCipher(key)
    x = datetime.datetime.now()
    text_to_encrypt = x.strftime("%Y%m%d%H%M%S")
    encrypted_text = aes_cipher.encrypt_string(text_to_encrypt)

    # if hasattr(models, 'Gmc12080101'):
    #     obj = models.Gmc12080101(
    #         secretekey=data['secret_key'],
    #         publickey=data['publickey'],
    #         encryptedsk=encrypted_text,
    #         created_by=data['created_by']
    #     )
    #     db.add(obj)
    #     db.commit()

    response_data = {
        "Encrypted Secret Key": encrypted_text,
    }
    return response_data
    # else:
    #     return "fail - Model not found"
