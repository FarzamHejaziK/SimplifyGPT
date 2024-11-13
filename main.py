from openai import OpenAI
from config.config_manager import ConfigManager
import argparse

config = ConfigManager()
client = OpenAI(
        api_key=config.get('openai.api_key')
    )

def load_system_prompt(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
    

system_prompt = load_system_prompt(config.get('openai.system_prompt_path'))


def get_completion(user_intent: str) -> str:
    formatted_prompt = system_prompt.format(user_intent=user_intent)

    completion = client.chat.completions.create(
        model=config.get('openai.model'),
        messages=[
            {
                "role": "system", 
                "content": formatted_prompt
            }
        ]
    )
    return completion.choices[0].message.content

def main():
    # Ask for user input
    print("\nWhat concept would you like to understand better?")
    user_intent = input("> ")
    
    print("\nGenerating explanation...\n")
    response = get_completion(user_intent)
    print(response)

if __name__ == "__main__":
    main()