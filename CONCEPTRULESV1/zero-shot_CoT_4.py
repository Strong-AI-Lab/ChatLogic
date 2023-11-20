import openai
import json
import csv
import re
import os
import random

def ai_function_generation(demo, context, question, model="gpt-4"):
    messages = [{"role": "system", "content": demo},
                {"role": "user", "content": f"Propositions: ```{context}```\nQuestion: ```{question}```"}]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0
    )

    return response.choices[0].message["content"]

def ai_function_cot_part2(demo, context, model="gpt-4"):
    messages = [{"role": "system", "content": demo},
                {"role": "user", "content": f"```{context}```"}]

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
    "zero-shot-CoT-part1": remove_spaces("""
    Please help me complete this multi-step logical reasoning task. 
    Answer whether this question is correct based on the propositions about facts and rules formed by these natural language propositions. 
    You should think through the question step by step, and show your full process. \n"""),
    "zero-shot-CoT-part2": remove_spaces("""
    Based on this thought process, please help me sum up only a number as the final answer (1 represents correct, 0 represents wrong).""")
}

openai.api_key = os.getenv("OPENAI_API_KEY")

def ZeroShotCoT_call1(demo, context, question, model="gpt-4"):
    return ai_function_generation(demo, context, question, model)

def ZeroShotCoT_call2(demo, context, model="gpt-4"):
    return ai_function_cot_part2(demo, context, model)

jsonl_file = "conceptrules_full_train.jsonl"

all_entries = []
with open(jsonl_file, "r", encoding="utf-8") as file:
    for line in file:
        all_entries.append(json.loads(line))

# Randomly select 100 entries from the loaded data
selected_entries = random.sample(all_entries, 100)

with open("V1-zeroshot-cot-4.csv", "w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["id", "response", "label"])  # Write header

    for entry in selected_entries:
        context = entry["context"]
        first_question = entry["questions"][0]  # Assuming the structure is similar
        question_text = first_question["text"]
        label = first_question["label"]
        response_part_1 = ZeroShotCoT_call1(template['zero-shot-CoT-part1'], context, question_text)
        print(response_part_1)
        response_part_2 = ZeroShotCoT_call2(template['zero-shot-CoT-part2'], response_part_1)
        print("Writing to CSV:", [first_question["id"], response_part_2, label])

        csv_writer.writerow([first_question["id"], response_part_2, label])
