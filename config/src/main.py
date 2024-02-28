import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import spacy


# Define the Pydantic model
class Item(BaseModel):
    text: str


# Load the pre-trained SpaCy model
nlp = spacy.load('nb_core_news_sm')

app = FastAPI()


@app.post("/process-text/")
def process_text(item: Item):
    doc = nlp(item.text)
    nouns = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN']]

    # Iterate over the tokens to find the first noun
    for token in doc:
        if token.pos_ in ['NOUN', 'PROPN']:  # Check if the token is a noun or a proper noun
            return {"first_noun": token.text}  # Return the first noun found as a string


if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
