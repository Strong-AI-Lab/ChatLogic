from datasets import load_dataset
import csv
import json

PARARULE_Plus_dataset = load_dataset("qbao775/PARARULE-Plus")

json_files = [PARARULE_Plus_dataset['train'], PARARULE_Plus_dataset['validation'], PARARULE_Plus_dataset['test']]
csv_file = "record.csv"

def extract_ids_to_csv(json_file, csv_file):
    id_list = []
    for item in json_file:
        id_value = item.get('id')
        if id_value:
            id_list.append(id_value)

    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows([[id_value] for id_value in id_list])


for json_file in json_files:
    extract_ids_to_csv(json_file, csv_file)

new_header = ['id', 'test_1', 'test_2', 'test_3', 'debug_time', 'python_code']

with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)
rows.insert(0, new_header)

with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)