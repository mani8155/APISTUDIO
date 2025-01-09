from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import datetime


class AESCipher:
    def __init__(self, key):
        self.key = key.encode('utf-8')
        self.iv = get_random_bytes(16)

    def encrypt_string(self, plain_text):
        cipher = AES.new(self.key, AES.MODE_CFB, iv=self.iv)
        encrypted_text = cipher.encrypt(pad(plain_text.encode('utf-8'), AES.block_size))
        return base64.b64encode(self.iv + encrypted_text).decode('utf-8')

    def decrypt_string(self, cipher_text):
        combined_data = base64.b64decode(cipher_text.encode('utf-8'))
        iv = combined_data[:16]
        encrypted_bytes = combined_data[16:]

        cipher = AES.new(self.key, AES.MODE_CFB, iv=iv)
        decrypted_text = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
        return decrypted_text.decode('utf-8')


def custom_api(db, models, data):
    data = {
        'created_by': data['created_by'],
        'publickey': data['publickey'],
        'secret_key': data['secret_key'],
    }

    key = data['secret_key']

    # Example Usage
    # key = "1226193703425550"
    aes_cipher = AESCipher(key)

    # text_to_encrypt = "1226193703425550"
    x = datetime.datetime.now()
    text_to_encrypt = x.strftime("%Y%m%d%H%M%S")
    encrypted_text = aes_cipher.encrypt_string(text_to_encrypt)
    print(f"Encrypted Text: {encrypted_text}")

    # decrypted_text = aes_cipher.decrypt_string(encrypted_text)
    # print(f"Decrypted Text: {decrypted_text}")

    if hasattr(models, 'Gmc12080101'):
        obj = models.Gmc12080101(
            secretekey=data['secret_key'],
            publickey=data['publickey'],
            encryptedsk=encrypted_text,
            created_by=data['created_by']
        )
        db.add(obj)
        db.commit()

        response_data = {
            "Encrypted Secret Key": encrypted_text,
        }
        return response_data
    else:
        return "fail - Model not found"
