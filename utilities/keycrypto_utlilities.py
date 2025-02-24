

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import boto3
import base64

from utilities.logger import setup_logging


logger = setup_logging()



def generate_rsa_keypair_with_pythoncrypto():
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

    # Generate public key
    public_key = private_key.public_key()

    # Serialize and save public key to file
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem, public_pem


def generate_rsa_keypair_with_kms(TARGET_AWS_KMS_ARN):
    kms_client = boto3.client('kms')

    response = kms_client.generate_data_key_pair(
        KeyId=TARGET_AWS_KMS_ARN,
        KeyPairSpec='RSA_2048',
    )
    # PrivateKeyCiphertextBlob, PrivateKeyPlaintext, PublicKey
    private_key = serialization.load_der_private_key(
        response['PrivateKeyPlaintext'],
        password=None
    )
    private_pem_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')

    public_key = serialization.load_der_public_key(response['PublicKey'])
    public_pem_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')
    
    return private_pem_key, public_pem_key
    