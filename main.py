from logger import setup_logging

logger = setup_logging()

def main():
    ...
    # add a python function that will use aws kms to create a asymetric keys locally
    

if __name__ == '__main__':
    logger.info("Application started")
    try:

        main()
    except Exception:
        logger.exception("Something went wrong")
    logger.info("Application finished without errors")