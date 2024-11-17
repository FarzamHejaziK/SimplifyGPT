from openai import OpenAI
from config.config_manager import ConfigManager
import logging

logger = logging.getLogger(__name__)
config = ConfigManager()
client = OpenAI(api_key=config.get('openai.api_key'))

def load_system_prompt(file_path: str) -> str:
    """Load system prompt from file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def get_completion(user_intent: str) -> str:
    system_prompt = load_system_prompt(config.get('openai.system_prompt_path'))
    formatted_prompt = system_prompt.format(user_intent=user_intent)

    completion = client.chat.completions.create(
        model=config.get('openai.model'),
        messages=[
            {
                "role": "system", 
                "content": formatted_prompt
            }
        ],
        temperature=config.get('chat.temperature'),
        max_tokens=config.get('chat.max_tokens')
    )

    return completion.choices[0].message.content 