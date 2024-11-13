from utils.helpers import get_completion, parse_yaml_response, display_explanation

def main():
    # Ask for user input
    print("\nWhat concept would you like to understand better?")
    user_intent = input("> ")
    
    print("\nGenerating explanation...\n")
    
    # Get raw response
    yaml_response = get_completion(user_intent)
    
    # Parse YAML response
    parsed_response = parse_yaml_response(yaml_response)
    
    # Display results
    if isinstance(parsed_response, dict):
        display_explanation(parsed_response, user_intent)
    else:
        print(parsed_response)

if __name__ == "__main__":
    main() 