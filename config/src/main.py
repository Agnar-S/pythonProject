import uvicorn
from pydantic import BaseModel
from starlette.middleware import _MiddlewareClass

import vectorbot as vb
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import vectorbot as vb



# Create an instance of the FastAPI class
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Define the Pydantic model
class Item(BaseModel):
    text: str


@app.post("/process-text/")
def process_text(item: Item):
    return vb.run(item.text)





if __name__ == "__main__":
    uvicorn.run(app, port=8001, host="0.0.0.0")
