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

JSON_filename = 'PARARULE_plus_step2_People_sample.json'
PY_filename = 'pyDatalog_processing.py'


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

# load the data
data = []
for file_name in json_files:
    with open(file_name, 'r', encoding='utf-8') as json_file:
        tmp = json.load(json_file)
        data.extend(tmp)
data = random.sample(data, 50)
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

# the basement without converting the propositions back to the code
accuracy = 0
for i in range(0, 50):
    try:
        # first time generate the code from propositions
        result_string = extract_string(batch_process(
            f"""{templates.templates['agent_engineer']}, Here are the propositions: {data[i]['context']} and the Question:{data[i]['question']},
                                {templates.templates['no_extra_content']}"""))
        # print(result_string)

        # save the code into the file
        with open(PY_filename, 'w') as file:
            file.write("{}".format(result_string))
        output = subprocess.check_output(['python', PY_filename], universal_newlines=True)
        print(f"output: {output}")
        if (output.strip() != '1' and output.strip() != '0'):
            continue
        else:
            accuracy += 1
    except Exception as e:
        continue

# test the accuracy if we add the back convertion part in to the framework
correct_num_flag0 = 0
correct_num_flag3 = 0
for i in range(0, 50):
    try:
        # first time generate the code from propositions
        result_string = extract_string(batch_process(
            f"""{templates.templates['agent_engineer']}, Here are the propositions: {data[i]['context']} and the Question:{data[i]['question']},
                                        {templates.templates['no_extra_content']}"""))
        # print(result_string)

        # convert code back 2 propositions
        propositions_generated = batch_process(
            f"""{templates.templates["agent_engineer_neg"]}, and the following is the generated code: {result_string}""")

        # Comparison
        # zero-shot CoT is here
        tag = batch_process(
            f"""{templates.templates['check_error_part1']}, and the original Propositions:{data[i]['context']}, and Question:{data[i]['question']}, the generated Propositions and Questions: {propositions_generated}""")
        tag_final = batch_process(
            f"""{templates.templates['check_error_part2']}, the following is the analysis processing: {tag}""")

        # print(f"tag: {tag}")
        # print(f"tag_final: {tag_final}")

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
            result_string = extract_string(batch_process(f"""{templates.templates['regeneration']},The original propositions are:{data[i]['context']}, and Question:{data[i]['question']}, and the following is the generated code: {result_string}, and the differences: {tag_final}"""))
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
        if int(output.strip()) == data[i]['label']:
            correct_num_flag3 += 1
        else:
            continue
    except Exception as e:
        continue

print(f"accuracy number: {accuracy}")
print(f"correct_num_0: {correct_num_flag0}")
print(f"correct_num_3: {correct_num_flag3}")


