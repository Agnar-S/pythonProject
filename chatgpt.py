import os
import sys
import spacy
import re
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain_community.vectorstores import Chroma
import constants
import time

# Load spaCy model with disabled components for efficiency
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

# Precompile regex patterns for efficiency
transition_phrases = ["Regarding", "Furthermore", "Additionally", "Note:"]
transition_phrases_pattern = re.compile(r"(?<!\.)\s(" + "|".join(transition_phrases) + ")")

os.environ["OPENAI_API_KEY"] = constants.APIKEY

PERSIST = False

# Implement caching mechanism for repeated queries (placeholder logic)
cache = {}


def preprocess_question(question):
    # Use spaCy's efficient processing
    doc = nlp(question)
    cleaned_question = " ".join(token.lemma_ for token in doc if not token.is_stop and not token.is_punct)
    return cleaned_question


def format_answer_with_bullets(answer):
    # Use compiled regex for replacing transition phrases
    answer = transition_phrases_pattern.sub(r". \1", answer)

    # Efficient sentence splitting
    items = re.split(r'(?<=[^A-Z].[.?]) (?=[A-Z])', answer)
    bullet_formatted_answer = "\n".join(f"• {item.strip()}" for item in items if item)

    return "Here are the responses with bullet points:\n\n" + bullet_formatted_answer


def construct_prompt(user_input):
    instruction = "You only answer questions related to permitted items in luggage at the airport."
    return f"{instruction}\n\nUser: {user_input}\nAI:"


# Main loop simplified for clarity
if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else None

    if PERSIST and os.path.exists("persist"):
        print("Reusing index...\n")
        vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
        index = VectorStoreIndexWrapper(vectorstore=vectorstore)
    else:
        loader = DirectoryLoader("data/")
        if PERSIST:
            index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory": "persist"}).from_loaders([loader])
        else:
            index = VectorstoreIndexCreator().from_loaders([loader])

    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model="gpt-3.5-turbo"),
        retriever=index.vectorstore.as_retriever(search_kwargs={"k": 92}),
    )

    chat_history = []
    while True:

        user_input = input("Prompt: ") if not query else query
        if user_input.lower() in ['quit', 'q', 'exit']:
            sys.exit()

        start_time = time.time()

        # Check cache before processing
        if user_input in cache:
            formatted_answer = cache[user_input]
        else:
            prompt = construct_prompt(user_input)
            query = preprocess_question(user_input)  # Adjust the logic here if necessary
            result = chain({"question": prompt, "chat_history": chat_history})  # Adjusted to send the entire prompt
            formatted_answer = format_answer_with_bullets(result['answer'])
            cache[user_input] = formatted_answer  # Update cache

        print(formatted_answer)
        end_time = time.time()
        result = end_time - start_time
        print("Time: ", result)
        chat_history.append((user_input, formatted_answer))
        query = None  # Reset query for the next loop iteration
