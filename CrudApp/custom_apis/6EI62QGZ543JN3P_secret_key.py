from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
from cryptography.hazmat.primitives import padding
from datetime import datetime, timedelta
import pytz


def custom_api(db, models, data):
    data = {
        'created_by': data['created_by'],
        'publickey': data['publickey'],
        'secret_key': data['secret_key'],
    }

    secret_key = data['secret_key']

    india_timezone = pytz.timezone('Asia/Kolkata')
    current_timestamp = datetime.now(india_timezone).strftime('%Y%m%d%H%M%S')

    validity_duration = timedelta(minutes=3)

    # Calculate the expiration time
    expiration_time = datetime.now(india_timezone) + validity_duration
    expiration_timestamp = expiration_time.strftime('%Y%m%d%H%M%S')

    # Combine API Secret Key, timestamp, and expiration time for encryption
    data_to_encrypt = f'{secret_key}{current_timestamp}{expiration_timestamp}'.encode('utf-8')

    # Pad the data to meet the block length requirements
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data_to_encrypt) + padder.finalize()

    # Encrypt the padded data using AES
    cipher = Cipher(algorithms.AES(secret_key.encode('utf-8')), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Convert the encrypted data to base64
    encrypted_data_base64 = base64.b64encode(encrypted_data).decode('utf-8')

    if hasattr(models, 'Gmc12080101'):
        obj = models.Gmc12080101(
            secretekey=data['secret_key'],
            publickey=data['publickey'],
            encryptedsk=encrypted_data_base64,
            created_by=data['created_by']
        )
        db.add(obj)
        db.commit()

        response_data = {
            "Encrypted Secret Key": encrypted_data_base64,
            "Expiration Time": expiration_time
        }
        return response_data
    else:
        return "fail - Model not found"

