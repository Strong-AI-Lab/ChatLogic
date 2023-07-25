def extract_adjectives(input_string):
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
                    adjectives = extract_adjectives(first_word)
                    first_is_list.extend(adjectives)

                second_is_index = sentence[first_is_index+3:].find("are")
                if second_is_index != -1:
                    second_word = sentence[first_is_index+3+second_is_index+4:].strip()
                    if second_word:
                        second_is_list.append(second_word)

        if "All" in sentence and "people are" in sentence:
            people_are_index = sentence.find("people are")
            if people_are_index != -1:
                first_word = sentence[3:people_are_index].strip()
                if first_word:
                    adjectives = extract_adjectives(first_word)
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

if __name__ == "__main__":
    sentences_str = "Fiona is high. Fiona is huge. Erin is little. Erin is short. Harry is smart. Alan is dull. Alan is rough. If someone is not big then they are dull. If someone is not sad then they are clever. If someone is smart then they are kind. If someone is kind and not poor then they are quiet. If someone is dull and not big then they are bad. If someone is bad then they are small. All small people are tiny. If someone is little and short then they are poor. If someone is poor and not kind then they are rough. If someone is rough then they are energetic. If someone is energetic then they are young. If someone is clever then they are nice. If someone is nice then they are wealthy. All wealthy people are kind. If someone is quiet then they are old. All old people are experienced."
    first_list, second_list = extract_words_from_sentences(sentences_str)
    print("The first list：", first_list)
    print("The second list：", second_list)

    print(find_unique_elements(first_list, second_list))