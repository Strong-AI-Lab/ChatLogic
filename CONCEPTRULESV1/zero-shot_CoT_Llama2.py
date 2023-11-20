import transformers
import torch
import re
import json
import csv
import random

# Define the Llama-2-7b model
model_name = "meta-llama/Llama-2-7b-chat-hf"
tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)
model = transformers.pipeline(
    "text-generation",
    model=model_name,
    torch_dtype=torch.float16,
    device_map="auto",  # Automatically choose the device (CPU/GPU)
)

# Function to remove extra spaces
def remove_spaces(text):
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'^ +| +$', '', text, flags=re.MULTILINE)
    return text

# Define the template for the prompt
template = {
    "zero-shot-CoT": remove_spaces("""
    Please help me complete this multi-step logical reasoning task. 
    Answer whether this question is correct based on the propositions about facts and rules formed by these natural language propositions. 
    You should think through the question step by step, and show your full process. 
    Based on this thought process, please help me sum up only a number as the final answer (1 represents correct, 0 represents wrong). 
    The Propositions and Questions are as follows: \n""")
}

# Function to process a single entry
def process_entry(context, question):
    prompt = template['zero-shot-CoT'] + f"Propositions: {context}\nQuestion: {question}"
    sequences = model(prompt, do_sample=True, top_k=10, num_return_sequences=1, max_length=2048)
    return sequences[0]['generated_text']

# Read and process the data
jsonl_file = "conceptrules_full_train.jsonl"
all_entries = []
with open(jsonl_file, "r", encoding="utf-8") as file:
    for line in file:
        all_entries.append(json.loads(line))

selected_entries = random.sample(all_entries, 100)

# Write the processed entries to a CSV file
with open("Llama2-7B-CoT.csv", "w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["question_id", "response", "label"])  # Header row

    for entry in selected_entries:
        context = entry["context"]
        first_question = entry["questions"][0]
        question_text = first_question["text"]
        label = first_question["label"]

        response = process_entry(context, question_text)
        csv_writer.writerow([first_question["id"], response, label])

        # Memory cleanup
        del response
        torch.cuda.empty_cache()  # Clear the CUDA cache if using GPU
