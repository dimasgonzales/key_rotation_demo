import boto3
from botocore.exceptions import ClientError

from utilities.logger import setup_logging


logger = setup_logging()


def create_secret(secret_value: str, secret_name: str) -> None:
    
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
    )

    try:
        logger.info(f"Creating new secret: {secret_name}")
        client.create_secret(
            Name=secret_name,
            SecretString=str(secret_value)
        )
        logger.info(f"Successfully created secret: {secret_name}")
    except ClientError as e:
        raise e

def get_secret(secret_name: str) -> str:

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']
    return secret

def put_secret(secret_value: str, secret_name: str) -> None:
    
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
    )

    try:
        logger.info(f"Attempting to update secret: {secret_name}")
        client.put_secret_value(
            SecretId=secret_name,
            SecretString=str(secret_value)
        )
        logger.info(f"Successfully updated secret: {secret_name}")
    except ClientError as e:
        raise e
    

def check_if_secret_exists(secret_name):
    
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
    )

    try:
        client.describe_secret(
            SecretId=secret_name
        )
        return True
    except ClientError as e:
        return False
        # raise e