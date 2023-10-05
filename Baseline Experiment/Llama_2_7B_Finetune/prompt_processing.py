import csv
import json
import re

json_files = [
    "../../PARARULE_plus_step2_Animal_sample.json",
    "../../PARARULE_plus_step3_Animal_sample.json",
    "../../PARARULE_plus_step4_Animal_sample.json",
    "../../PARARULE_plus_step5_Animal_sample.json",
    "../../PARARULE_plus_step2_People_sample.json",
    "../../PARARULE_plus_step3_People_sample.json",
    "../../PARARULE_plus_step4_People_sample.json",
    "../../PARARULE_plus_step5_People_sample.json"
]

def remove_spaces(text):
    # Replace multiple spaces with a single space
    text = re.sub(r' +', ' ', text)
    # Remove leading and trailing spaces from each line
    text = re.sub(r'^ +| +$', '', text, flags=re.MULTILINE)
    return text

with open("Llama2-7B-finetune-prompt.csv", "w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    for json_file in json_files:
        step = '_'.join(json_file.split("_")[2:4])
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            for entry in data:
                context = entry["context"]
                question = entry["question"]
                label = entry["label"]
                # Replace this with your actual function call
                prompt = f"""instruction: Based on the closed world assumption, please help me complete a multi-step logical reasoning task (judge true or not). Please help me answer whether the question is correct or not based on the facts and rules formed by these natural language propositions. You should just return me one number as the final answer (1 for true and 0 for wrong) without providing any reasoning process. The input contains all propositions, each sentence is an independent proposition, and the question, and the output is the answer to the question.,\
                            input: Propositions: {context}, Question: {question}, output:"""
                csv_writer.writerow([remove_spaces(prompt)])
                csv_writer.writerow([label])
