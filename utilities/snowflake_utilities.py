
import os

import snowflake.connector

from utilities.logger import setup_logging

logger = setup_logging()


def update_snowflake_user_public_key(target_user, public_key):
    """Connect to Snowflake and update the specified user's public key.
    This function establishes a connection to Snowflake and updates the RSA public key
    for the specified user using an ALTER USER command.
    Args:
        target_user (str): The username whose public key needs to be updated.
        public_key (str): The new RSA public key to be set for the user.
    Raises:
        Exception: If there is any error during the connection or key update process.
            The specific exception is logged and re-raised.
    Example:
        >>> public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A..."
        >>> update_snowflake_user_public_key("SNOW_USER", public_key)
    """
    logger.debug(f"Attempting to update public key for user: {target_user}")
    cursor = None
    conn = None
    try:
        # Connect to Snowflake
        conn = establish_snowflake_connection()
        cursor = conn.cursor()
        
        # Alter user command to set public key
        alter_user_sql = f"ALTER USER {target_user} SET RSA_PUBLIC_KEY='{public_key}'"
        logger.debug(f"Executing SQL: {alter_user_sql}")
        cursor.execute(alter_user_sql)

        logger.info(f"Successfully updated public key for user: {target_user}")

    except Exception as e:
        logger.error(f"Failed to update public key for user {target_user}: {str(e)}", exc_info=True)
        raise
    finally:
        if cursor:
            logger.debug("Closing cursor")
            cursor.close()
        if conn:
            logger.debug("Closing connection")
            conn.close()

def establish_snowflake_connection():
    """Establish connection to Snowflake using environment variables."""
    logger.debug("Attempting to establish Snowflake connection")
    try:
        conn = snowflake.connector.connect(
            user=os.getenv('SNOWFLAKE_USER'),
            password=os.getenv('SNOWFLAKE_PASSWORD'),
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
            database=os.getenv('SNOWFLAKE_DATABASE'),
            schema=os.getenv('SNOWFLAKE_SCHEMA')
        )
        logger.info("Successfully established Snowflake connection")
        return conn
    except snowflake.connector.errors.DatabaseError as e:
        logger.error("Failed to establish Snowflake connection", exc_info=True)
        raise
