import openai
import json
import csv
import re
import os
import random

def ai_function_generation(demo, context, question, model="gpt-3.5-turbo"):
    messages = [{"role": "system", "content": demo},
                {"role": "user", "content": f"Propositions: ```{context}```\nQuestion: ```{question}```"}]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0
    )

    return response.choices[0].message["content"]

def remove_spaces(text):
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'^ +| +$', '', text, flags=re.MULTILINE)
    return text

template = {
    "ConceptRules_baseline": remove_spaces("""
    Please help me complete a multi-step logical reasoning task. 
    Please help me answer whether the question is correct or not based on the facts and rules formed by these natural language propositions. 
    You should just return me one number as the final answer (1 for true and 0 for wrong) and also provide reasoning process. 
    The Propositions and Questions are as follows: \n""")
}

openai.api_key = os.getenv("OPENAI_API_KEY")

def Baseline_ChatGPT_call(demo, context, question, model="gpt-3.5-turbo"):
    return ai_function_generation(demo, context, question, model)

# Read the JSON Lines file
jsonl_file = "ConceptRules/conceptrules_full_train.jsonl"

all_entries = []
with open(jsonl_file, "r", encoding="utf-8") as file:
    for line in file:
        all_entries.append(json.loads(line))

# Randomly select 100 entries from the loaded data
selected_entries = random.sample(all_entries, 100)

with open("ConceptRulesV1.csv", "w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["id", "response", "label"])  # Write header

    for entry in selected_entries:
        context = entry["context"]
        first_question = entry["questions"][0]
        question_text = first_question["text"]
        label = first_question["label"]
        response = Baseline_ChatGPT_call(template['ConceptRules_baseline'], context, question_text)

        csv_writer.writerow([first_question["id"], response, label])
