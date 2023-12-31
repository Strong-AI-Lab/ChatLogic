from transformers import AutoTokenizer, pipeline
import transformers
import torch
import re
import json
import csv
import random

model = "meta-llama/Llama-2-7b-chat-hf"

def remove_spaces(text):
    # Replace multiple spaces with a single space
    text = re.sub(r' +', ' ', text)
    # Remove leading and trailing spaces from each line
    text = re.sub(r'^ +| +$', '', text, flags=re.MULTILINE)
    return text

template = {
    "ConceptRules_baseline": remove_spaces("""
    Please help me complete a multi-step logical reasoning task. 
    Please help me answer whether the question is correct or not based on the facts and rules formed by these natural language propositions. 
    You should just return me one number as the final answer (1 for true and 0 for wrong) and also provide reasoning process. 
    The Propositions and Questions are as follows: \n""")
}

tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    torch_dtype=torch.float16,
    device_map="auto",
)

def batch_process(text):
    sequences = pipeline(
        text,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=2048,
    )
    return sequences[0]['generated_text']

jsonl_file = "ConceptRulesV2/conceptrules_v2_full_train.jsonl"

# First read all entries into a list
all_entries = []
with open(jsonl_file, "r", encoding="utf-8") as file:
    for line in file:
        all_entries.append(json.loads(line))

# Randomly select 100 entries
selected_entries = random.sample(all_entries, 100)

# Process the selected entries
with open("Llama2-7B.csv", "w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["question_id", "response", "label"])  # Write header

    for entry in selected_entries:
        context = entry["context"]
        for question in entry["questions"]:
            question_text = question["text"]
            label = question["label"]
            responses = batch_process(f"Instructions: ```{template['ConceptRules_baseline']}```Propositions: ```{context}```\nQuestion: ```{question_text}```")
            csv_writer.writerow([question["id"], responses, label])
