import yaml
import logging
from typing import Union, Dict

logger = logging.getLogger(__name__)

def clean_yaml_string(yaml_str: str) -> str:
    """Clean up YAML string by removing code block markers and normalizing content."""
    lines = yaml_str.split('\n')
    
    if lines and any(lines[0].startswith('```')):
        lines = lines[1:]
    if lines and any(lines[-1].startswith('```')):
        lines = lines[:-1]
    
    cleaned_str = '\n'.join(lines).strip()
    
    cleaned_str = (cleaned_str
        .replace('\u2018', "'")
        .replace('\u2019', "'")
        .replace('\u201c', '"')
        .replace('\u201d', '"')
        .replace('\u2013', '-')
        .replace('\u2014', '--')
    )
    
    return cleaned_str

def parse_yaml_response(yaml_str: str) -> Union[Dict, str]:
    """Parse YAML string to dictionary."""
    try:
        cleaned_str = yaml_str
        if cleaned_str.startswith('```yaml'):
            cleaned_str = cleaned_str[7:]
        elif cleaned_str.startswith('```'):
            cleaned_str = cleaned_str[3:]
        if cleaned_str.endswith('```'):
            cleaned_str = cleaned_str[:-3]
        
        cleaned_str = cleaned_str.strip()
        cleaned_str = clean_yaml_string(cleaned_str)
        return yaml.safe_load(cleaned_str)
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML: {e}\nInput that caused error:\n{'-' * 50}\n{cleaned_str}\n{'-' * 50}")
        return yaml_str 