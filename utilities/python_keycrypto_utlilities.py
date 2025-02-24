

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

from utilities.logger import setup_logging


logger = setup_logging()



def generate_rsa_keypair(private_key_path='keys/private_key.pem', public_key_path='keys/public_key.pem'):
    """
    Creates an RSA key pair and saves them to specified file paths.

    This function generates a 2048-bit RSA key pair using cryptography library.
    The private key is saved in PKCS8 format with no encryption, and the public
    key is saved in SubjectPublicKeyInfo format. Both are PEM encoded.

    Args:
        private_key_path (str, optional): File path where the private key will be saved.
            Defaults to 'keys/private_key.pem'.
        public_key_path (str, optional): File path where the public key will be saved.
            Defaults to 'keys/public_key.pem'.

    Note:
        The function will create the necessary directories if they don't exist.
        The private key is saved without encryption - take appropriate security measures.

    Returns:
        None

    Raises:
        OSError: If there are permission or disk space issues when creating directories
            or writing files.
    """
    # Ensure directories exist
    os.makedirs(os.path.dirname(private_key_path), exist_ok=True)
    os.makedirs(os.path.dirname(public_key_path), exist_ok=True)

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # Serialize and save private key to file
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    with open(private_key_path, 'wb') as f:
        f.write(private_pem)

    # Generate public key
    public_key = private_key.public_key()

    # Serialize and save public key to file
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(public_key_path, 'wb') as f:
        f.write(public_pem)
    return private_pem, public_pem