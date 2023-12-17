import json
import random
import os
import subprocess
import openai
import csv
import call_openai_API
import templates

# Assume other functions (such as Generation, BackConversion, etc.) remain unchanged
# Initialize OpenAI API client
openai.api_key = os.getenv("OPENAI_API_KEY")

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

# Function definition in original code

def extract_string(input_string):
    left_boundary = 'import'
    right_boundary = ')'

    start_index = input_string.find(left_boundary)
    end_index = input_string.rfind(right_boundary, start_index)

    if start_index != -1 and end_index != -1:
        extracted_string = input_string[start_index:end_index + 1]
        return extracted_string.strip()

    return None

def Judgement(demo, question, model):
    result_string = call_openai_API.ai_generation_check(demo, question, model="gpt-3.5-turbo")
    return result_string

# Complete Communication with ChatGPT
def Generation(demo, context, question, requirements, model="gpt-3.5-turbo"):
    result_string = call_openai_API.ai_function_generation(demo, context, question, requirements, model)
    return result_string

def BackConvertion(demo, code, model="gpt-3.5-turbo"):
    result_string = call_openai_API.ai_function_backconvertion(demo, code, model)
    return result_string

# Communication(templates.templates["agent_engineer"], PARARULE_Plus.PARARULE_Plus_dataset['train'][200]['context'], PARARULE_Plus.PARARULE_Plus_dataset['train'][200]['question'], templates.templates["no_extra_content"], "gpt-3.5-turbo")

def Adjustment(demo, code, error_message, model="gpt-3.5-turbo"):
    result_string = call_openai_API.ai_generation_adjustment(demo, code, error_message, model)
    return result_string

def Extraction(demo, text, model="gpt-3.5-turbo"):
    result_string = call_openai_API.ai_function_extraction(demo, text, model)
    return result_string

def Comparison(demo, original, generated, model="gpt-3.5-turbo"):
    result_string = call_openai_API.ai_function_comparison(demo, original, generated, model)
    return result_string

def Regeneration(demo, context, code, text, model="gpt-3.5-turbo"):
    result_string = call_openai_API.ai_function_regeneration(demo, context, code, text, model)
    return result_string



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
        # generate the code
        result_string = extract_string(Generation(templates.templates["agent_engineer"], context, question_text, templates.templates["no_extra_content"]))
        print(result_string)
        # convert code back 2 propositions
        propositions_generated = BackConvertion(templates.templates["agent_engineer_neg"], result_string)

        # Comparison
        # zero-shot CoT is here
        tag = Comparison(templates.templates["check_error_part1"],
                         f"Propositions:{context}, Question:{question_text}", propositions_generated)
        tag_final = Extraction(templates.templates["check_error_part2"], tag)
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
                result_string = extract_string(Adjustment(templates.templates["adjustment_agent"],
                                                          result_string, output))
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
            print(Regeneration(templates.templates["regeneration"],
                                                        f"Propositions:{context}, Question:{question_text}",
                                                        result_string, tag_final))
            result_string = extract_string(Regeneration(templates.templates["regeneration"],
                                                        f"Propositions:{context}, Question:{question_text}",
                                                        result_string, tag_final))
            print(f"regeneration result: {result_string}")
            with open(PY_filename, 'w') as file:
                file.write("{}".format(result_string))
            output = subprocess.check_output(['python', PY_filename], universal_newlines=True)
            flag = 0
            while (output.strip() != "1" and output.strip() != "0"):
                result_string = extract_string(Adjustment(templates.templates["adjustment_agent"],
                                                          result_string, output))
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
