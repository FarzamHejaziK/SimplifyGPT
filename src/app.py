import streamlit as st
import time
import logging
import sys
from pathlib import Path

# Setup logging and paths
logger = logging.getLogger(__name__)
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import local modules
from utils import setup_logging, get_completion, parse_yaml_response, display_explanation
from rendition.page_config import render_page_config
from rendition.content import render_input_section, render_explanation
from rendition.document import render_document, render_images_grid

def main():
    render_page_config()
    setup_logging()
    
    user_intent = render_input_section()
    
    if user_intent:
        with st.spinner("Generating explanation..."):
            try:
                start_time = time.time()
                yaml_response = get_completion(user_intent)
                parsed_response = parse_yaml_response(yaml_response)
                
                if isinstance(parsed_response, dict):
                    output_folder = display_explanation(parsed_response, user_intent)
                    logger.info(f"Output folder: {output_folder}")
                    
                    st.success(f"Generated explanation in {time.time() - start_time:.2f} seconds!")
                    render_explanation(parsed_response, output_folder)
                
                else:
                    st.error("Failed to generate explanation. Please try again.")
                    logger.error(f"Failed to parse YAML response: {yaml_response}")
            
            except Exception as e:
                st.error("An error occurred while generating the explanation.")
                logger.error(f"Error in Streamlit app: {e}", exc_info=True)

if __name__ == "__main__":
    main() 