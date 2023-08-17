import json
import csv
import re
import os

def remove_spaces(text):
    # Replace multiple spaces with a single space
    text = re.sub(r' +', ' ', text)
    # Remove leading and trailing spaces from each line
    text = re.sub(r'^ +| +$', '', text, flags=re.MULTILINE)
    return text

template = {
    "ChatGPT_baseline": remove_spaces("""Based on the closed world assumption, please help me complete a multi-step logical reasoning task. Please help me answer whether the question is correct or not based on the facts and rules formed by these natural language propositions.
                                            You should just return me one number as the final answer  (1 for true and 0 for wrong) and also provide reasoning process. The Propositions and Questions are as follows: Propositions: """)
}



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
with open("GPT4.csv", "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Types", "id", "Prompts", "label"])  # Write header

    for json_file in json_files:
        type = '_'.join(json_file.split("_")[2:4])
        with open(json_file, "r") as f:
            data = json.load(f)
            for entry in data:
                context = entry["context"]
                question = entry["question"]
                label = entry["label"]
                id = entry["id"]
                prompt = template["ChatGPT_baseline"] + context + "And the question is: " + question
                csv_writer.writerow([type, id, prompt, label])