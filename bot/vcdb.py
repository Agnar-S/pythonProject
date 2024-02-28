import weaviate
import json
import constants
import time

client = weaviate.Client(
    url="https://embeddings-90t5a7p8.weaviate.network/",  # Replace with your endpoint
    auth_client_secret=weaviate.auth.AuthApiKey(api_key="Kz4fjQ308k0r5CiHSk3GUvpinVCPehRHmapo"),
    # Replace w/ your Weaviate instance API key
    additional_headers={
        "X-OpenAI-Api-Key": constants.APIKEY  # Replace with your inference API key
    }
)


def query(item):
    # Use f-string to insert the 'item' variable into the query
    # Also, ensure that the item is properly quoted within the query
    query_item = f"""
    {{
      Get {{
        TravelItem(where: {{operator: Equal, path: ["description"], valueString: "{item}"}}) {{
          itemName
          description
          allowedInHandBaggage
          allowedInCheckedBaggage
        }}
      }}
    }}
    """
    return query_item

def get_description(query):
    try:
        start_time = time.time()
        # Execute the query
        result = client.query.raw(query)
        # Extract the description field
        description = result["data"]["Get"]["TravelItem"][0]["description"]
        # Print the results
        end_time = time.time()
        result = end_time - start_time
        print(f"Vectordb call: {result} sek")
        return description

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error"
