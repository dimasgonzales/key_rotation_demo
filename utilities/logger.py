import logging
import logging.handlers
from pathlib import Path
import threading


class DuplicateFilter(logging.Filter):
    """Filter that eliminates duplicate log messages."""
    
    def __init__(self):
        super().__init__()
        self.seen_messages = set()
        self.lock = threading.Lock()
    
    def filter(self, record):
        # Get the formatted message
        msg = record.getMessage()
        with self.lock:
            # If message is new, add it and return True to allow logging
            if msg not in self.seen_messages:
                self.seen_messages.add(msg)
                return True
            # Return False to prevent logging if message was seen before
            return False



def setup_logging(log_level=logging.INFO):
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    # Set botocore to only log errors
    logging.getLogger('botocore').setLevel(logging.ERROR)
    
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Add duplicate filter
    duplicate_filter = DuplicateFilter()
    logger.addFilter(duplicate_filter)
    
    # Formatting
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=1024 * 1024,  # 1MB
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger
