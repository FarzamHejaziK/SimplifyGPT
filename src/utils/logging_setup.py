import logging
import sys
import os
from datetime import datetime
from pathlib import Path

def setup_logging():
    """Configure logging to output to timestamped file in output directory."""
    # Remove any existing handlers first
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    
    # Set the logging level
    root_logger.setLevel(logging.DEBUG)
    
    # Create formatters
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Create output directory if it doesn't exist
    base_dir = Path(__file__).parent.parent.parent  # Go up to project root
    logs_dir = Path(base_dir) / "logs"
    error_logs_dir = logs_dir / "errors"  # Separate directory for error logs
    
    # Create directories
    logs_dir.mkdir(parents=True, exist_ok=True)
    error_logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Create timestamped log files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    debug_log_file = logs_dir / f"debug_{timestamp}.log"
    error_log_file = error_logs_dir / f"error_{timestamp}.log"
    
    # Setup debug file handler (all logs)
    file_handler = logging.FileHandler(debug_log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    
    # Setup error file handler (only ERROR and above)
    error_file_handler = logging.FileHandler(error_log_file)
    error_file_handler.setFormatter(formatter)
    error_file_handler.setLevel(logging.ERROR)
    
    # Setup console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)
    
    # Add all handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_file_handler)
    root_logger.addHandler(console_handler)
    
    # Test log messages
    root_logger.info(f"Logging session started. Debug log: {debug_log_file}")
    root_logger.info(f"Errors will be saved to: {error_log_file}")
    root_logger.debug("Debug logging is enabled")
    
    return root_logger