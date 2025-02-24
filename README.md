# Asymmetric Key Rotator

This Python script automates the rotation of asymmetric PEM key pairs used by Snowflake Service Accounts for authentication. It handles the complete lifecycle of key rotation including generation, secure storage in AWS Secrets Manager, and Snowflake user updates.

The following sequence diagram illustrates the key rotation process:

```mermaid
sequenceDiagram
    participant Script
    participant AWSKMS
    participant AWSSecretsManager
    participant Snowflake

   Script->>AWSKMS: Request Key Generation
   AWSKMS->>Script: Return 2048-bit RSA Key Pair
   Script->>AWSSecretsManager: Check Secret Exists
   alt Secret Exists
      AWSSecretsManager->>Script: Update existing Secret with new Keys
   else No Secret Found
      AWSSecretsManager->>Script: Create a new Secret with new Keys
   end
   Script->>Snowflake: Alter Snowflake User with new Public Key
```


## Features

- Generates 2048-bit RSA key pairs with strong encryption
- Securely stores keys in AWS Secrets Manager
- Automatically updates Snowflake user credentials
- Comprehensive logging with rotation support
- AWS KMS integration for additional security

## Prerequisites

- Python 3.x
- AWS API Access with permissions to 
   - AWS Secrets Manager
   - AWS KMS
- Snowflake account with admin privileges
- [uv](https://github.com/astral-sh/uv) - Modern Python package installer

## Installation

1. Clone the repository
2. Setup environment variables
3. Install and run using uv:
```bash
uv run main.py
```

Dependencies are automatically managed through inline script declarations:

main.py:
```python
# /// script
# dependencies = [
#     "boto3",
#     "botocore",
#     "python-dotenv"
# ]
# ///
```

## Configuration

### Environment Variables

Copy .env.sample to .env:
```bash
cp .env.sample .env
```

Update the `.env` file with your credentials:


### AWS Secrets Manager

The script uses a standardized naming convention for secrets:
- Private key: `snowflake_service_accounts/{TARGET_SNOWFLAKE_USERNAME}/private_key`
- Public key: `snowflake_service_accounts/{TARGET_SNOWFLAKE_USERNAME}/public_key`

Both secrets must either exist or not exist together. The script will:
- Create both secrets if neither exists
- Update both secrets if both exist
- Raise an error if only one secret exists (invalid state)

### Snowflake Configuration

Ensure your Snowflake service account has the necessary permissions to:
- Create and manage key pairs
- Update user authentication settings
- Access required databases and schemas

## Usage



```bash
uv run main.py
```

The script will:
1. Generate new PEM key pairs
2. Store the PEM keys in AWS Secrets Manager
   - Update existing secret if it exists
   - Create new secret if it doesn't exist
3. Update the Snowflake user with the new public PEM key

## Logging

The application uses a comprehensive logging system that includes:
- Console output for immediate feedback
- Rotating file logs stored in `logs/app.log`
- Log rotation at 1MB with 3 backup files maintained
- Timestamp and log level information
- Detailed error tracking
