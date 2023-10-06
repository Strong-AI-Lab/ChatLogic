import openai
import json
import csv
import re
import os

def ai_function_generation(demo, context, question, requirements, model = "gpt-3.5-turbo"):
    # parse args to comma separated string
    messages = [{"role": "system",
                "content": demo},
                {"role": "user",
                "content": f"Propositions: ```{context}```\nQuestion: ```{question}```"}]

    response = openai.ChatCompletion.create(
        model = model,
        messages = messages,
        temperature = 0
    )

    return response.choices[0].message["content"]


def remove_spaces(text):
    # Replace multiple spaces with a single space
    text = re.sub(r' +', ' ', text)
    # Remove leading and trailing spaces from each line
    text = re.sub(r'^ +| +$', '', text, flags=re.MULTILINE)
    return text

template = {
    "ChatGPT_baseline": remove_spaces("""Based on the closed world assumption, please help me complete a multi-step logical reasoning task. Please help me answer whether the question is correct or not based on the facts and rules formed by these natural language propositions. 
                                            You should just return me one number as the final answer  (1 for true and 0 for wrong) and also provide reasoning process. The Propositions and Questions are as follows: \n""")
}

openai.api_key = api_key = os.getenv("OPENAI_API_KEY")


def Baseline_ChatGPT_call(demo, context, question, model = "gpt-3.5-turbo"):
    return ai_function_generation(demo, context, question, model)



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
with open("ChatGPT.csv", "w", newline="", encoding="utf-8") as csv_file:
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
                response = Baseline_ChatGPT_call(template['ChatGPT_baseline'], context, question)

                csv_writer.writerow([step, response, label])