from utils import setup_logging, get_completion, parse_yaml_response, display_explanation
import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)

def main():
    start_time = time.time()
    logger.info("Starting application")
    
    try:
        # Ask for user input
        print("\nWhat concept would you like to understand better?")
        user_intent = input("> ")
        input_time = time.time()
        logger.info(f"Received user input in {input_time - start_time:.2f}s: {user_intent}")
        
        print("\nGenerating explanation...\n")
        
        # Get raw response
        yaml_response = get_completion(user_intent)
        completion_time = time.time()
        logger.info(f"Generated OpenAI response in {completion_time - input_time:.2f}s")
        
        # Parse YAML response
        parsed_response = parse_yaml_response(yaml_response)
        parsing_time = time.time()
        logger.info(f"Parsed YAML in {parsing_time - completion_time:.2f}s")
        
        # Display results
        if isinstance(parsed_response, dict):
            output_folder = display_explanation(parsed_response, user_intent)
            display_time = time.time()
            logger.info(f"Generated document and images in {display_time - parsing_time:.2f}s")
            logger.info(f"Output saved to: {output_folder}")
        else:
            print(parsed_response)
            logger.error("Failed to parse response as YAML")
        
        # Log total execution time
        end_time = time.time()
        total_time = end_time - start_time
        
        logger.info("\nExecution Summary:")
        logger.info(f"├── Input Time: {input_time - start_time:.2f}s")
        logger.info(f"├── OpenAI Generation: {completion_time - input_time:.2f}s")
        logger.info(f"├── YAML Parsing: {parsing_time - completion_time:.2f}s")
        logger.info(f"├── Document & Images: {display_time - parsing_time:.2f}s")
        logger.info(f"└── Total Time: {total_time:.2f}s")
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}", exc_info=True)
        end_time = time.time()
        logger.error(f"Failed after {end_time - start_time:.2f}s")
        raise

if __name__ == "__main__":
    setup_logging()
    main() 