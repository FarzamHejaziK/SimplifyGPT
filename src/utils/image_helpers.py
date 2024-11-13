import os
import requests
from openai import OpenAI
from config.config_manager import ConfigManager
import logging
from typing import Union, Dict

logger = logging.getLogger(__name__)

def generate_and_save_images(explanation_dict: Dict, user_intent: str):
    """Generate DALL-E images for each step and save them."""
    logger.info(f"Starting image generation for concept: {user_intent}")
    folder_name = os.path.join("images", f"{user_intent}")
    
    try:
        os.makedirs(folder_name, exist_ok=True)
        logger.debug(f"Created directory: {folder_name}")
        
        config = ConfigManager()
        client = OpenAI(api_key=config.get('openai.api_key'))
        
        for step in explanation_dict['steps']:
            try:
                logger.info(f"Generating image for step {step['step_number']}")
                
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=step['image_description'],
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                
                image_url = response.data[0].url
                image_data = requests.get(image_url).content
                image_path = f"{folder_name}/step_{step['step_number']}.png"
                
                with open(image_path, 'wb') as f:
                    f.write(image_data)
                logger.info(f"Saved image for step {step['step_number']}")
                
            except Exception as e:
                logger.error(f"Error generating image for step {step['step_number']}: {e}", exc_info=True)
                
        logger.info(f"Completed image generation. Images saved in: {folder_name}")
        return folder_name
        
    except Exception as e:
        logger.error(f"Error in image generation process: {e}", exc_info=True)
        raise 