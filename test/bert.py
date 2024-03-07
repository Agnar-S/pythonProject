from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Initialize the tokenizer and model from the pre-trained versions
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

# Function to generate text from a prompt
def generate_text(prompt, max_length=50, num_return_sequences=1):
    # Encode the prompt text to tensor
    input_ids = tokenizer.encode(prompt, return_tensors='pt')

    # Generate text using the model
    output_sequences = model.generate(
        input_ids=input_ids,
        max_length=max_length + len(input_ids[0]),
        temperature=1.0,
        top_k=50,
        top_p=0.95,
        repetition_penalty=1.0,
        do_sample=True,
        num_return_sequences=num_return_sequences,
    )

    # Decode the generated text
    generated_texts = []
    for generated_sequence in output_sequences:
        generated_sequence = generated_sequence.tolist()
        text = tokenizer.decode(generated_sequence, clean_up_tokenization_spaces=True)
        text = text[: text.rfind(prompt) + len(prompt)]
        generated_texts.append(text)

    return generated_texts

# Example usage
prompt = "Once upon a time"
generated_texts = generate_text(prompt, max_length=50, num_return_sequences=3)

for i, text in enumerate(generated_texts, 1):
    print(f"Generated Text {i}:\n{text}\n")
