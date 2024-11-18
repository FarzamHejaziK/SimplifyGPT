import asyncio
import aiohttp
import time
from typing import Dict, List
import os
import logging
from openai import OpenAI
from config.config_manager import ConfigManager
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

logger = logging.getLogger(__name__)

def generate_dalle_image(client: OpenAI, prompt: str) -> str:
    """Generate DALL-E image in a separate thread."""
    config = ConfigManager()
    # Remove first word from prompt
    prompt_words = prompt.split()
    if len(prompt_words) > 1:
        prompt = ' '.join(prompt_words[1:])
        logger.info(f"Generating DALL-E image with prompt: {prompt}")
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=config.get('image_generation.size'),
        quality=config.get('image_generation.quality'),
        n=1,
    )
    return response.data[0].url

async def generate_single_image(
    client: OpenAI, 
    step: Dict, 
    folder_name: str,
    session: aiohttp.ClientSession,
    executor: ThreadPoolExecutor,
    start_time: float
) -> None:
    """Generate and save a single image asynchronously."""
    step_num = step['step_number']
    try:
        logger.info(f"[Step {step_num}] Starting image generation at {time.time() - start_time:.2f}s")
        
        # Run DALL-E generation in thread pool
        loop = asyncio.get_event_loop()
        image_url = await loop.run_in_executor(
            executor, 
            generate_dalle_image, 
            client, 
            step['image_description']
        )
        
        logger.info(f"[Step {step_num}] Got DALL-E response at {time.time() - start_time:.2f}s")
        
        # Download image
        async with session.get(image_url) as response:
            logger.info(f"[Step {step_num}] Starting image download at {time.time() - start_time:.2f}s")
            image_data = await response.read()
            logger.info(f"[Step {step_num}] Completed download at {time.time() - start_time:.2f}s")
        
        # Save image
        image_path = f"{folder_name}/step_{step_num}.png"
        with open(image_path, 'wb') as f:
            f.write(image_data)
            
        logger.info(f"[Step {step_num}] Saved image at {time.time() - start_time:.2f}s")
        
    except Exception as e:
        logger.error(f"[Step {step_num}] Error at {time.time() - start_time:.2f}s: {e}", exc_info=True)

async def generate_images_async(explanation_dict: Dict, folder_name: str) -> None:
    """Generate all images concurrently."""
    config = ConfigManager()
    client = OpenAI(api_key=config.get('openai.api_key'))
    start_time = time.time()
    
    logger.info(f"Starting concurrent image generation for {len(explanation_dict['steps'])} steps")
    
    # Create thread pool for DALL-E API calls
    with ThreadPoolExecutor(max_workers=10) as executor:
        async with aiohttp.ClientSession() as session:
            tasks = [
                generate_single_image(client, step, folder_name, session, executor, start_time)
                for step in explanation_dict['steps']
            ]
            logger.info(f"Created {len(tasks)} concurrent tasks at {time.time() - start_time:.2f}s")
            await asyncio.gather(*tasks)
            
    logger.info(f"All tasks completed at {time.time() - start_time:.2f}s")

def generate_and_save_images(explanation_dict: Dict, user_intent: str) -> str:
    """Generate DALL-E images for each step and save them."""
    start_time = time.time()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create unique folder name with timestamp
    sanitized_intent = "".join(c for c in user_intent if c.isalnum() or c in (' ', '-', '_')).strip()
    sanitized_intent = sanitized_intent.replace(' ', '_').lower()
    folder_name = os.path.join("images", f"{timestamp}_{sanitized_intent}")
    
    logger.info(f"Starting parallel image generation for concept: {user_intent}")
    
    try:
        os.makedirs(folder_name, exist_ok=True)
        logger.debug(f"Created directory: {folder_name}")
        
        # Run async code
        asyncio.run(generate_images_async(explanation_dict, folder_name))
        
        total_time = time.time() - start_time
        logger.info(f"Completed all image generations in {total_time:.2f} seconds")
        logger.info(f"Images saved in: {folder_name}")
        
        return folder_name
        
    except Exception as e:
        logger.error(f"Error in image generation process: {e}", exc_info=True)
        raise