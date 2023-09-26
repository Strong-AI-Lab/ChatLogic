import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
import re



def extract_adjectives_in_conditional_sentence(input_string):
    words = input_string.split()
    if "and" in words:
        words.remove("and")
    return words

def extract_words_from_sentences(sentences_str):
    sentences = sentences_str.split(".")
    print(sentences)
    first_is_list = []
    second_is_list = []

    for sentence in sentences:
        sentence = sentence.strip()
        if "If" in sentence and "is" in sentence and "then" in sentence and "are" in sentence:
            first_is_index = sentence.find("is")
            if first_is_index != -1 and "then" in sentence:
                first_word = sentence[first_is_index + 3:sentence.find("then")].strip()
                if first_word:
                    adjectives = extract_adjectives_in_conditional_sentence(first_word)
                    first_is_list.extend(adjectives)

                second_is_index = sentence[first_is_index+3:].find("are")
                if second_is_index != -1:
                    second_word = sentence[first_is_index+3+second_is_index+4:].strip()
                    if second_word:
                        second_is_list.append(second_word)

        elif "All" in sentence and "people are" in sentence:
            people_are_index = sentence.find("people are")
            if people_are_index != -1:
                first_word = sentence[3:people_are_index].strip()
                if first_word:
                    adjectives = extract_adjectives_in_conditional_sentence(first_word)
                    first_is_list.extend(adjectives)

                second_word = sentence[people_are_index + 10:].strip()
                if second_word:
                    second_is_list.append(second_word)

        elif "people are" in sentence:
            people_are_index = sentence.find("people are")
            if people_are_index != -1:
                first_word = sentence[:people_are_index].strip().lower()
                if first_word:
                    adjectives = extract_adjectives_in_conditional_sentence(first_word)
                    first_is_list.extend(adjectives)

                second_word = sentence[people_are_index + 10:].strip()
                if second_word:
                    second_is_list.append(second_word)

    while "not" in first_is_list:
        unique_set = set(first_is_list)
        unique_set.discard("not")
        first_is_list = list(unique_set)

    while "not" in second_is_list:
        unique_set = set(second_is_list)
        unique_set.discard("not")
        second_is_list = list(unique_set)

    return first_is_list, second_is_list


def find_unique_elements(list1, list2):
    unique_elements = []

    for element in list1:
        if element not in list2:
            unique_elements.append(element)

    return unique_elements



def extract_adjectives(words, target_name):
    tagged_words = pos_tag(words)

    adjectives = []
    name_found = False
    verb_found = False

    for word, tag in tagged_words:
        if tag == 'NNP' and word == target_name:
            name_found = True
        elif name_found and not verb_found and tag.startswith('VB'):
            verb_found = True
        elif verb_found and tag.startswith('JJ'):
            adjectives.append(word)
        else:
            name_found = False
            verb_found = False

    return adjectives

def extract_names(words):
    tagged_words = pos_tag(words)

    names = []
    current_name = []

    for word, tag in tagged_words:
        if tag == 'NNP':
            current_name.append(word)
        elif current_name:
            names.append(" ".join(current_name))
            current_name = []

    if current_name:
        names.append(" ".join(current_name))

    return names

def is_subject_verb_adjective(sentence):
    pattern = r"^(NNP\s)*(VBZ\s)"
    tagged_sentence = " ".join(tag for word, tag in sentence)
    return re.match(pattern, tagged_sentence)

def extract_names_and_attributes(text):
    sentences = sent_tokenize(text)
    dic = {}
    for sentence in sentences:
        if is_subject_verb_adjective(pos_tag(word_tokenize(sentence))):
            words = word_tokenize(sentence)
            name = "".join(extract_names(words))
            if name:
                if name not in dic:
                    dic[name] = []
                adjectives = extract_adjectives(words, name)
                dic[name].extend(adjectives)

    return dic

def create_output_string(dct, word_list):
    output_string = ""
    for name, attributes in dct.items():
        for word in word_list:
            if word not in attributes:
                output_string += f"{name} is not {word}. "
    return output_string.strip()


if __name__ == "__main__":
    sentences_str = "Anne is huge. Anne is big. Anne is high. Harry is little. Harry is short. Alan is nice. Alan is quiet. Alan is kind. Erin is rough. Erin is poor. Erin is sad. Huge people are nice. If someone is little and short then they are small. If someone is rough and poor then they are dull. If someone is nice and quiet then they are wealthy. All small people are thin. All nice people are quiet. All wealthy people are smart. All dull people are bad."
    first_list, second_list = extract_words_from_sentences(sentences_str)
    print("The first list：", first_list)
    print("The second list：", second_list)
    print(extract_names_and_attributes(sentences_str))
    print(find_unique_elements(first_list, second_list))

    sentences = ""

    for name in extract_names_and_attributes(sentences_str).keys():
        # for each words in the list
        for word in find_unique_elements(first_list, second_list):
            # Generate a sentence if the word is not in the value of the current key of the dictionary
            if word not in extract_names_and_attributes(sentences_str)[name]:
                sentences = sentences + (f" {name} is not {word}.")

    print(sentences)
    # call this py file to return a string base on cwa (People)
    # print(create_output_string(extract_names_and_attributes(sentences_str), find_unique_elements(first_list, second_list)))