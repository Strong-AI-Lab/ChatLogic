from transformers import AutoTokenizer
import transformers
import torch
import re
import json
import csv

model = "meta-llama/Llama-2-7b-chat-hf"

def remove_spaces(text):
    # Replace multiple spaces with a single space
    text = re.sub(r' +', ' ', text)
    # Remove leading and trailing spaces from each line
    text = re.sub(r'^ +| +$', '', text, flags=re.MULTILINE)
    return text

template = {
    "Llama2_baseline": remove_spaces("""Based on the closed world assumption, please help me complete a multi-step logical reasoning task (judge true or not). Please help me answer whether the question is correct or not based on the facts and rules formed by these natural language propositions. 、
                                            You should just return me one number as the final answer  (1 for true and 0 for wrong) and providing reasoning process simply. The Propositions and Questions are as follows: \n""")
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


# List of json file names
json_files = [
    "../PARARULE_plus_step2_Animal_sample.json",
    "../PARARULE_plus_step3_Animal_sample.json",
    "../PARARULE_plus_step4_Animal_sample.json",
    "../PARARULE_plus_step5_Animal_sample.json",
    "../PARARULE_plus_step2_People_sample.json",
    "../PARARULE_plus_step3_People_sample.json",
    "../PARARULE_plus_step4_People_sample.json",
    "../PARARULE_plus_step5_People_sample.json"
]

# Open the CSV file for writing
with open("Llama2-7B.csv", "w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["step", "return", "label"])  # Write header

    for json_file in json_files:
        step = '_'.join(json_file.split("_")[2:4])
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            for entry in data:
                context = entry["context"]
                question = entry["question"]
                label = entry["label"]
                # Replace this with your actual function call
                responses = batch_process(f"Instructions: ```{template['Llama2_baseline']}```Propositions: ```{context}```\nQuestion: ```{question}```")

                csv_writer.writerow([step, responses, label])
