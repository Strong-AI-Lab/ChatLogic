import ast
import json
import time
import call_openai_API
import templates
import openai
import openai_API_keys
import PARARULE_Plus


# Initialize the OpenAI API client
openai.api_key = openai_API_keys.OPENAI_API_KEY


# Complete Communication with ChatGPT
def Communication(demo, context, question, requirements, model):

    result_string = call_openai_API.ai_function_generation(demo, context, question, requirements, model)
    print(f"{result_string}")

Communication(templates.templates["agent_engineer"], PARARULE_Plus.PARARULE_Plus_dataset['train'][200]['context'], PARARULE_Plus.PARARULE_Plus_dataset['train'][200]['question'], templates.templates["no_extra_content"], "gpt-3.5-turbo")