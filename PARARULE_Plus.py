from datasets import load_dataset
import json

# import the dataset PARARULE_plus from huggingface
PARARULE_Plus_dataset = load_dataset("qbao775/PARARULE-Plus")
Data_step2 = []
Data_step3 = []
Data_step4 = []
Data_step5 = []
for i in PARARULE_Plus_dataset['train']:
    if i['meta']['QDep'] == '2':
        Data_step2.append(i)
    if i['meta']['QDep'] == '3':
        Data_step3.append(i)
    if i['meta']['QDep'] == '4':
        Data_step4.append(i)
    if i['meta']['QDep'] == '5':
        Data_step5.append(i)
for i in PARARULE_Plus_dataset['validation']:
    if i['meta']['QDep'] == '2':
        Data_step2.append(i)
    if i['meta']['QDep'] == '3':
        Data_step3.append(i)
    if i['meta']['QDep'] == '4':
        Data_step4.append(i)
    if i['meta']['QDep'] == '5':
        Data_step5.append(i)
for i in PARARULE_Plus_dataset['test']:
    if i['meta']['QDep'] == '2':
        Data_step2.append(i)
    if i['meta']['QDep'] == '3':
        Data_step3.append(i)
    if i['meta']['QDep'] == '4':
        Data_step4.append(i)
    if i['meta']['QDep'] == '5':
        Data_step5.append(i)

# Create a dataset to store QCat == 0
filename = 'PARARULE_plus_step2.json'
with open(filename, 'w') as file:
    json.dump(Data_step2, file)

filename = 'PARARULE_plus_step3.json'
with open(filename, 'w') as file:
    json.dump(Data_step3, file)

filename = 'PARARULE_plus_step4.json'
with open(filename, 'w') as file:
    json.dump(Data_step4, file)

filename = 'PARARULE_plus_step5.json'
with open(filename, 'w') as file:
    json.dump(Data_step5, file)
# PARARULE_Plus_dataset = [item for item in PARARULE_Plus_dataset if item['train']['meta']['QCat'] == '0']
# for i in range(3):
#     print(PARARULE_Plus_dataset[i])
# print(PARARULE_Plus_dataset['train'][200]['label'])
# with the following index PARARULE_Plus_dataset['train'][0/1/2/3...]
# {'id': 'NegationRule-Animal-D2-3082',
# 'context': 'The bald eagle is sleepy. '
#             'The bald eagle is rough. '
#             'The leopard is heavy. '
#             'The leopard is fierce. '
#             'The bald eagle visits the rabbit. '
#             'The leopard sees the dog. '
#             'The rabbit is nice. '
#             'The dog is nice. '
#             'The dog is furry. '
#             'The dog is lovely. '
#             'If something is not nice then it needs the rabbit. '
#             'If something needs the rabbit then it is slow. '
#             'If something is not round then it is heavy. '
#             'If something is not strong then it is cute. '
#             'If something is furry then it is lovely. '
#             'If something is lovely and not big then it is small. '
#             'If something is heavy and not round then it is awful. '
#             'If something is sleepy and rough then it is big. '
#             'If something is big and not lovely then it is fierce. '
#             'All cute animals are beautiful.',
#             'question': 'The bald eagle is not awful.',
#             'label': 0, 'meta': {'QDep': '2', 'QCat': '0_0_not_notTrue'}}