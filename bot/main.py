import sys
import time
import requests

# Implement caching mechanism for repeated queries (placeholder logic)
cache = {}


# Main loop simplified for clarity
if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else None
    url="http://127.0.0.1:8000/process-text/"
    chat_history = []
    while True:
        start_time = time.time()
        user_input = input("Prompt: ") if not query else query
        if user_input.lower() in ['quit', 'q', 'exit']:
            sys.exit()

        start_time = time.time()

        # Check cache before processing
        if user_input in cache:
            formatted_answer = cache[user_input]
        else:

            data = {
                'text': user_input
            }
            # Sending a POST request with the JSON payload
            formatted_answer = requests.post(url, json=data)

        print(formatted_answer.text)



