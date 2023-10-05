from peft import PeftModel
from transformers import AutoTokenizer, LlamaForCausalLM
import torch
import csv
import json
import re

# run this code on VM machine (server from the lab)


# json_files = [
#     "PARARULE_plus_step2_Animal_sample.json"
# ]

# "PARARULE_plus_step3_Animal_sample.json",
# "PARARULE_plus_step4_Animal_sample.json",
# "PARARULE_plus_step5_Animal_sample.json"
# "../PARARULE_plus_step2_People_sample.json",
#     "../PARARULE_plus_step3_People_sample.json",
#     "../PARARULE_plus_step4_People_sample.json",
#     "../PARARULE_plus_step5_People_sample.json"



device = torch.device('cuda:0')
# load the original llm
model_path = "meta-llama/Llama-2-7b-hf"
model = LlamaForCausalLM.from_pretrained(model_path, trust_remote_code=True).half().to(device)
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = PeftModel.from_pretrained(model, "lora-alpaca").half()
prompt = "instruction: Based on the closed world assumption, please help me complete a multi-step logical reasoning task (judge true or not). Please help me answer whether the question is correct or not based on the facts and rules formed by these natural language propositions. You should just return me one number as the final answer (1 for true and 0 for wrong) without providing any reasoning process. The input contains all propositions, each sentence is an independent proposition, and the question, and the output is the answer to the question., input: Propositions: The dinosaur is lazy. The dinosaur is rough. The wolf is heavy. The wolf is fierce. The dinosaur visits the squirrel. The wolf likes the rabbit. The squirrel is quiet. The rabbit is quiet. The rabbit is furry. The rabbit is small. If something is not quiet then it attacks the squirrel. If something attacks the squirrel then it is dull. If something is not smart then it is heavy. If something is not strong then it is beautiful. If something is furry then it is small. If something is small and not big then it is lovely. If something is heavy and not smart then it is awful. If something is lazy and rough then it is big. If something is big and not small then it is fierce. All beautiful animals are cute., Question: The dinosaur is awful., output:"
inputs = tokenizer(prompt, return_tensors="pt").to(device)
generate_ids = model.generate(input_ids=inputs.input_ids, max_length=2048)
print(tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0])

# model.generate(tokenizer, text, history=[])


# # load LoRA hyperpara to the original LLM
# model = PeftModel.from_pretrained(model, "lora-alpaca").half()
# model.generate(tokenizer, text, history=[])

# from transformers import Pipeline, LlamaForCausalLM, AutoTokenizer
# import torch
# import csv
# import json

# # 初始化模型和tokenizer
# model_path = "meta-llama/Llama-2-7b-hf"
# model = LlamaForCausalLM.from_pretrained(model_path, trust_remote_code=True).half()
# tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

# # define pipeline
# generate_pipeline = Pipeline(model=model, tokenizer=tokenizer)

# # process multiple json files
# json_files = [
#     "PARARULE_plus_step2_Animal_sample.json",
#     "PARARULE_plus_step3_Animal_sample.json",
#     "PARARULE_plus_step4_Animal_sample.json",
#     "PARARULE_plus_step5_Animal_sample.json"
# ]

# # initialize the csv file
# with open("Llama2-7B-finetune-animal.csv", "w", newline="", encoding="utf-8") as csv_file:
#     csv_writer = csv.writer(csv_file)
#     csv_writer.writerow(["step", "return", "label"])  # Write header

#     # process each json file
#     for json_file in json_files:
#         step = '_'.join(json_file.split("_")[2:4])
#         with open(json_file, "r", encoding="utf-8") as f:
#             data = json.load(f)
#             for entry in data:
#                 context = entry["context"]
#                 question = entry["question"]
#                 label = entry["label"]
#                 prompt = f"""instruction: Based on the closed world assumption, please help me complete a multi-step logical reasoning task (judge true or not). Please help me answer whether the question is correct or not based on the facts and rules formed by these natural language propositions. You should just return me one number as the final answer (1 for true and 0 for wrong) without providing any reasoning process. The input contains all propositions, each sentence is an independent proposition, and the question, and the output is the answer to the question.,\
#                             input: Propositions: {context}, Question: {question}, output:"""

#                 # generate the context
#                 generated_text = generate_pipeline(prompt, max_length=2048)

#                 # write into csv file
#                 csv_writer.writerow([step, generated_text[0]['generated_text'], label])