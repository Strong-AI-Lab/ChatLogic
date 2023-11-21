from transformers import AutoTokenizer
import transformers
import torch
import re
import json
import csv
import templates
import subprocess
import random

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

def extract_string(input_string):
    left_boundary = 'import'
    right_boundary = ')'

    start_index = input_string.find(left_boundary)
    end_index = input_string.rfind(right_boundary, start_index)

    if start_index != -1 and end_index != -1:
        extracted_string = input_string[start_index:end_index + 1]
        return extracted_string.strip()

    return None


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


# Define JSON Lines file name
# This position will be changed according to different data set statistics
jsonl_file = "ConceptRulesV2/conceptrules_v2_full_train.jsonl"

# 从JSON Lines文件中加载数据
data = []
with open(jsonl_file, "r", encoding="utf-8") as file:
    for line in file:
        entry = json.loads(line)
        first_question_data = entry['questions'][0]  # 提取第一个问题
        entry['questions'] = [first_question_data]  # 更新entry只包含第一个问题
        data.append(entry)


# select 100 records randomly
data = random.sample(data, 100)


PY_filename = 'pyDatalog_processing.py'


# # Open the CSV file for writing
# with open("Llama2-7B-ChatLogic.csv", "w", newline="", encoding="utf-8") as csv_file:
#     csv_writer = csv.writer(csv_file)
#     csv_writer.writerow(["step", "return", "label"])  # Write header
#
#     for json_file in json_files:
#         step = '_'.join(json_file.split("_")[2:4])
#         with open(json_file, "r", encoding="utf-8") as f:
#             data = json.load(f)
#             for entry in data:
#                 context = entry["context"]
#                 question = entry["question"]
#                 label = entry["label"]
#                 # Replace this with your actual function call
#                 responses = batch_process(f"Instructions: ```{template['Llama2_baseline']}```Propositions: ```{context}```\nQuestion: ```{question}```")
#
#                 csv_writer.writerow([step, responses, label])

# count variables
accuracy = 0
correct_num_flag0 = 0
correct_num_flag3 = 0

for entry in data:
    context = entry['context']
    question_data = entry['questions'][0]
    question_text = question_data['text']
    label = question_data['label']
    try:
        # first time generate the code from propositions
        result_string = extract_string(batch_process(
            f"""{templates.templates['agent_engineer']}, Here are the propositions: {context} and the Question:{question_text},
                                {templates.templates['no_extra_content']}"""))
        print(result_string)

        # convert code back 2 propositions
        propositions_generated = batch_process(
            f"""{templates.templates["agent_engineer_neg"]}, and the following is the generated code: {result_string}""")

        # Comparison
        # zero-shot CoT is here
        # Comparison
        # zero-shot CoT is here
        tag = batch_process(
            f"""{templates.templates['check_error_part1']}, and the original Propositions:{context}, and Question:{question_text}, the generated Propositions and Questions: {propositions_generated}""")
        tag_final = batch_process(
            f"""{templates.templates['check_error_part2']}, the following is the analysis processing: {tag}""")

        # if it pass the comparison
        print(f"tag: {tag}")
        print(f"tag_final: {tag_final}")
        # if it pass the comparison
        if "true" in tag_final:
            print("no need to regenerate")
            flag = 0
            with open(PY_filename, 'w') as file:
                file.write("{}".format(result_string))
            output = subprocess.check_output(['python', PY_filename], universal_newlines=True)
            print(f"output: {output}")
            while (output.strip() != "1" and output.strip() != "0"):
                result_string = extract_string(batch_process(f"""{templates.templates['adjustment_agent']}, and here is the generated code: {result_string}, and the error message: {output}"""))
                with open(PY_filename, 'w') as file:
                    file.write("{}".format(result_string))
                print("reprocessing...")
                output = subprocess.check_output(['python', PY_filename], universal_newlines=True)
                print("New output:" + output)
                print(type(output))
                if flag == 0 and (output.strip() == "1" or output.strip() == "0"):
                    correct_num_flag0 += 1
                flag += 1
                if (flag == 3):
                    break
        else:
            print("enter the regeneration part")
            # regenaration
            result_string = extract_string(batch_process(f"""{templates.templates['regeneration']},The original propositions are:{context}, and Question:{question_text}, and the following is the generated code: {result_string}, and the differences: {tag_final}"""))
            print(f"regeneration result: {result_string}")
            with open(PY_filename, 'w') as file:
                file.write("{}".format(result_string))
            output = subprocess.check_output(['python', PY_filename], universal_newlines=True)
            flag = 0
            while (output.strip() != "1" and output.strip() != "0"):
                result_string = extract_string(batch_process(f"""{templates.templates['adjustment_agent']}, and here is the generated code: {result_string}, and the error message: {output}"""))
                with open(PY_filename, 'w') as file:
                    file.write("{}".format(result_string))
                print("reprocessing...")
                output = subprocess.check_output(['python', PY_filename], universal_newlines=True)
                print("New output:" + output)
                print(type(output))
                if flag == 0 and (output.strip() == "1" or output.strip() == "0"):
                    correct_num_flag0 += 1
                flag += 1
                if (flag == 3):
                    break

        # check correctness
        # if (output.strip() != '1' and output.strip() != '0'):
        #     correct_num_flag0 += 1
        if int(output.strip()) == label:
            correct_num_flag3 += 1
        else:
            continue
    except Exception as e:
        print(f"Extract error: {e}")
        continue

print(f"accuracy number: {accuracy}")
print(f"correct_num_0: {correct_num_flag0}")
print(f"correct_num_3: {correct_num_flag3}")