import sys
import time
import requester
import vcdb

# Implement caching mechanism for repeated queries (placeholder logic)
cache = {}

# Main loop simplified for clarity
if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else None

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
            noun = requester.get_nouns(user_input)
            # Parse the JSON string into a Python dictionary
            first_noun = noun["first_noun"]

            item_description = vcdb.get_description(vcdb.query(first_noun))

            print(item_description)
            end_time = time.time()
            print("Total time: ", end_time - start_time)
