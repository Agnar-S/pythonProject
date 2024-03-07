import torch
from transformers import BertForQuestionAnswering, BertTokenizer

# Load the tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

question = "Can i bring a knife"
context = "Respond with the word that is being talked about in the question"

inputs = tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="pt")
input_ids = inputs["input_ids"].tolist()[0]

with torch.no_grad():
    outputs = model(**inputs)
    answer_start_scores, answer_end_scores = outputs.start_logits, outputs.end_logits

# Get the most likely beginning and end of answer
answer_start = torch.argmax(answer_start_scores)
answer_end = torch.argmax(answer_end_scores) + 1  # Add 1 since the end index is exclusive

answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))

print(f"Question: {question}")
print(f"Answer: {answer}")
