import json
import random


input_files = ["PARARULE_plus_step2_Animal.json", "PARARULE_plus_step3_Animal.json",
               "PARARULE_plus_step4_Animal.json", "PARARULE_plus_step5_Animal.json",
               "PARARULE_plus_step2_People.json", "PARARULE_plus_step3_People.json",
               "PARARULE_plus_step4_People.json", "PARARULE_plus_step5_People.json"]
output_files = ["PARARULE_plus_step2_Animal_sample.json", "PARARULE_plus_step3_Animal_sample.json",
               "PARARULE_plus_step4_Animal_sample.json", "PARARULE_plus_step5_Animal_sample.json",
               "PARARULE_plus_step2_People_sample.json", "PARARULE_plus_step3_People_sample.json",
               "PARARULE_plus_step4_People_sample.json", "PARARULE_plus_step5_People_sample.json"]


for input_file, output_file in zip(input_files, output_files):
    with open(input_file, "r") as json_file:
        json_data_list = json.load(json_file)

    random_sample = random.sample(json_data_list, 40)

    with open(output_file, "w") as output_file:
        json.dump(random_sample, output_file)