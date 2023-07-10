import json
import call_openai_API
import templates
import openai
import openai_API_keys
import subprocess

# Initialize the OpenAI API client
openai.api_key = openai_API_keys.OPENAI_API_KEY
#Define the file name
JSON_filename = 'PARARULE_plus_QCat0.json'
PY_filename = 'pyDatalog_processing.py'

# Complete Communication with ChatGPT
def Communication(demo, context, question, requirements, model):

    result_string = call_openai_API.ai_function_generation(demo, context, question, requirements, model)
    return result_string

# Communication(templates.templates["agent_engineer"], PARARULE_Plus.PARARULE_Plus_dataset['train'][200]['context'], PARARULE_Plus.PARARULE_Plus_dataset['train'][200]['question'], templates.templates["no_extra_content"], "gpt-3.5-turbo")


with open(JSON_filename, 'r') as file:
    data = json.load(file)

correct_num = 0
for i in range(10):
    try:
        result_string = Communication(templates.templates["agent_engineer"], data[i]['context'],
                        data[i]['question'],
                        templates.templates["no_extra_content"], "gpt-3.5-turbo")
        print(result_string)
        with open(PY_filename, 'w') as file:
            file.write("{}".format(result_string))
        print("processing...")
        try:
            output = subprocess.check_output(['python', PY_filename], universal_newlines=True)
            if int(output.strip()) == data[i]['label']:
                correct_num += 1
            else:
                continue
            print(correct_num)
        except subprocess.TimeoutExpired:
            continue
    except Exception as e:
        continue
print(correct_num/20)