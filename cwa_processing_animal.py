import json
import re

animal_name = ['the bald eagle', 'the tiger', 'the bear', 'the lion', 'the wolf', 'the crocodile', 'the dinosaur',
               'the snake', 'the leopard']
animal_name_1 = ['the cat', 'the dog', 'the mouse', 'the rabbit', 'the squirrel']
animal_relations = ['is', 'is not']
animal_relations_1 = ['likes', 'chases', 'needs', 'visits', 'attacks', 'sees']
# animal_relations_1_1 = {'does not like', 'does not chase', 'does not need', 'does not visit', 'does not eat'}
animal_attributes_1 = ['kind', 'quiet', 'round', 'nice', 'smart']
animal_attributes_2 = ['dull', 'rough', 'lazy', 'slow', 'sleepy']

animal_attributes_3 = ['furry', 'small', 'cute', 'lovely', 'beautiful']
animal_attributes_4 = ['big', 'strong', 'awful', 'fierce', 'heavy']


def split_sentences(text):
    return re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)

animal_names = animal_name + animal_name_1
animal_attributes = animal_attributes_1 + animal_attributes_2 + animal_attributes_3 + animal_attributes_4
animal_relations = animal_relations + animal_relations_1


def sentence_processing(text):
    # 初始化输出字典和两个空列表
    facts = {}
    rules_condition = []  # 存储规则的条件部分（if部分）
    rules_consequence = []  # 存储规则的结论部分（then部分）

    # 分割文本为句子列表
    sentences = split_sentences(text)

    # 遍历每个句子并进行处理
    for sentence in sentences:
        # 对于 "动物1 is 属性" 句型
        if any(animal in sentence for animal in animal_names) and " is " in sentence and any(
                attr in sentence for attr in animal_attributes) and " is not " not in sentence and "If" not in sentence:
            parts = sentence.split(" is ")
            animal = parts[0].strip()
            attribute = parts[1].replace(".", "").strip()
            if animal not in facts:
                facts[animal] = []
            facts[animal].append(attribute)


        # 对于 "If something is 属性1 then it is 属性2" 句型
        elif "If" in sentence and "then" in sentence and " is not " not in sentence and " and not " not in sentence and " and " not in sentence:
            parts = sentence.split(" then ")
            condition_parts = parts[0].replace("If ", "").split(" is ")
            if len(condition_parts) == 2:
                condition = condition_parts[1].strip()  # 获取属性1
                consequence = parts[1].replace("it is ", "").replace(".", "").strip()  # 获取属性2

                # 将属性添加到对应的列表中
                rules_condition.append(condition)
                rules_consequence.append(consequence)

        # 对于 "If something is not 属性1 then it is 属性2" 句型
        elif "If" in sentence and "then" in sentence and " is not " in sentence and " and not " not in sentence and " and " not in sentence:
            parts = sentence.split(" then ")
            condition = parts[0].replace("If ", "").split(" is not ")[1].split(" and ")[0].strip()  # 获取属性1
            consequence = parts[1].replace("it is ", "").replace(".", "").strip()  # 获取属性2

            # 将属性添加到对应的列表中
            rules_condition.append(condition)
            rules_consequence.append(consequence)

        # 句型 "If something is 属性1 and not 属性2 then it is 属性3"
        elif "if" in sentence.lower() and "and not" in sentence and "then" in sentence and sum(
                attribute in sentence for attribute in animal_attributes) > 2:
            attributes_in_sentence = [attribute for attribute in animal_attributes if attribute in sentence]
            if len(attributes_in_sentence) == 3:
                rules_condition.extend(attributes_in_sentence[:2])
                rules_consequence.append(attributes_in_sentence[2])

        # 句型 "If something is 属性1 and 属性2 then it is 属性3"
        elif "if" in sentence.lower() and "and" in sentence and "then" in sentence and sum(
                attribute in sentence for attribute in animal_attributes) > 2:
            attributes_in_sentence = [attribute for attribute in animal_attributes if attribute in sentence]
            if len(attributes_in_sentence) == 3:
                rules_condition.extend(attributes_in_sentence[:2])
                rules_consequence.append(attributes_in_sentence[2])

        # 句型 "All 属性1 animals are 属性2"
        elif "all" in sentence.lower() and "animals are" in sentence and sum(
                attribute in sentence for attribute in animal_attributes) == 2:
            attributes_in_sentence = [attribute for attribute in animal_attributes if attribute in sentence]
            if len(attributes_in_sentence) == 2:
                rules_condition.append(attributes_in_sentence[0])
                rules_consequence.append(attributes_in_sentence[1])

    return facts, rules_condition, rules_consequence


def find_unique_elements(list1, list2):
    unique_elements = []

    for element in list1:
        if element not in list2:
            unique_elements.append(element)

    return unique_elements

def preprocessing(text):
    facts, rules_condition, rules_consequence = sentence_processing(text)

    sentences = ""

    for name in facts.keys():
        # for each words in the list
        for word in find_unique_elements(rules_condition, rules_consequence):
            # Generate a sentence if the word is not in the value of the current key of the dictionary
            if word not in facts[name]:
                sentences = sentences + (f"{name} is not {word}.")
    return sentences + " " + text



if __name__ == "__main__":
    json_files = [
        "PARARULE_plus_step2_Animal_sample.json",
        "PARARULE_plus_step3_Animal_sample.json",
        "PARARULE_plus_step4_Animal_sample.json",
        "PARARULE_plus_step5_Animal_sample.json",
        ]

    # Iterate over each JSON file
    for file_name in json_files:
        # Load the JSON data from file
        with open(file_name, 'r') as file:
            data = json.load(file)

        # Extract context from each data entry, preprocess, and update the data
        for entry in data:
            original_context = entry['context']
            preprocessed_context = preprocessing(original_context)
            entry['context'] = f"{preprocessed_context}"

        # Write the updated data back to the JSON file
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
