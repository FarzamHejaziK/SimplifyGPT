import os
import yaml
from dotenv import load_dotenv

class ConfigManager:
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._config is None:
            self._load_config()

    def _load_config(self):
        load_dotenv()
        
        config_path = 'config/initial_config.yaml'
        with open(config_path, 'r') as f:
            self._config = yaml.safe_load(f)
            
        # Replace environment variables
        if self._config['openai']['api_key'].startswith('${'):
            env_var = self._config['openai']['api_key'][2:-1]  # Remove ${ and }
            self._config['openai']['api_key'] = os.getenv(env_var)

    def get(self, key_path):
        keys = key_path.split('.')
        value = self._config
        for key in keys:
            value = value[key]
        return value 