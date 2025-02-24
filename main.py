# /// script
# dependencies = [
#     "boto3",
#     "botocore",
#     "python-dotenv",
#     "cryptography",
# ]
# ///


from utilities.keycrypto_utlilities import generate_rsa_keypair_with_kms
from utilities.aws_secrets_utilities import create_secret, put_secret, check_if_secret_exists
# from utilities.snowflake_utilities import update_snowflake_user_public_key
from utilities.logger import setup_logging
import os
from dotenv import load_dotenv

logger = setup_logging()

def main():
    load_dotenv()

    TARGET_SNOWFLAKE_USER = os.getenv("TARGET_SNOWFLAKE_USER")
    TARGET_AWS_KMS_ARN = os.getenv("TARGET_AWS_KMS_ARN")

    private_pem_key, public_pem_key = generate_rsa_keypair_with_kms(TARGET_AWS_KMS_ARN)

    # check if an AWS Secrets Manager exists for the target user
    # if not, create one
    # if it does, update it
    privatekey_secretname = f"snowflake_service_accounts/{TARGET_SNOWFLAKE_USER}/private_key"
    publickey_secretname = f"snowflake_service_accounts/{TARGET_SNOWFLAKE_USER}/public_key"

    if check_if_secret_exists(privatekey_secretname) and check_if_secret_exists(publickey_secretname): # TODO implement check for existing secret
        put_secret(
            secret_name=privatekey_secretname,
            secret_value=private_pem_key,
        )
        put_secret(
            secret_name=publickey_secretname,
            secret_value=public_pem_key,
        )
    elif check_if_secret_exists(privatekey_secretname) or check_if_secret_exists(publickey_secretname):
        raise ValueError("XOR condition not met. This should not happen. Please check that the secrets are created correctly.")
    else:
        create_secret(
            secret_name=privatekey_secretname,
            secret_value=private_pem_key,
        )

        create_secret(
            secret_name=publickey_secretname,
            secret_value=public_pem_key,
        )
    
    # TODO: implement Snowflake user update with public key
    # update_snowflake_user_public_key(
    #     user=TARGET_SNOWFLAKE_USER,
    #     public_key=public_pem_key,
    # )





if __name__ == '__main__':
    logger.info("Application started")
    try:
        main()
    except Exception:
        logger.exception("Something went wrong")
    logger.info("Application finished")