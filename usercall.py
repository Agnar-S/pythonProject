import time

from openai import OpenAI

api_key = "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"
client = OpenAI(api_key=api_key)
assistant_id = "asst_bCgyobnuzVlIig6TWQoGkgb3"




def api_call(user_message, assistant):
    # Create a new thread
    thread = client.beta.threads.create()

    client.beta.threads.messages.create(thread_id=thread.id, role="user", content=user_message)
    # Initiate a run with the assistant
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant)



    # Polling the run status until it's completed
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run_status.status == 'completed':
            break
        elif run_status.status in ['failed', 'cancelled']:
            print("Run did not complete successfully.")
            break
        time.sleep(0.1)  # Sleep for a short interval before checking again

    # Once the run is completed, list all messages in the thread
    messages = client.beta.threads.messages.list(thread_id=thread.id)

    # Filter and print the assistant's responses
    for message in messages.data:
        if message.role == "assistant":
            print("Assistant's response:", message.content[0].text.value)

        return message.content[0].text.value