# Use an official Python runtime as a parent image
FROM python:3.11

WORKDIR /neural-api

COPY requirements.txt .
COPY ./src ./src
# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Download the SpaCy model
RUN python -m spacy download nb_core_news_sm
# Run your script
CMD ["python", "./src/main.py"]