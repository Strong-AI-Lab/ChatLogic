import re

def remove_spaces(text):
    # Replace multiple spaces with a single space
    text = re.sub(r' +', ' ', text)
    # Remove leading and trailing spaces from each line
    text = re.sub(r'^ +| +$', '', text, flags=re.MULTILINE)
    return text

templates = {
    "agent_engineer": remove_spaces("""You are an engineer proficient in pyDatalog programming. I hope you learn the problem-solving process provided below and follow this process to complete new tasks.\n \
                            Task: Please help me translate the following natural language(Propositions and Questions) into executable pyDatalog code, meeting the following requirements: \n \
                            1. Phrases/sentences with the same meaning need to use the same variable name. \n \
                            2. Only output pyDatalog code and do not include any other explanatory text in your response. \n \
                            3. Save the judgment result ```(1/0)``` of the question into a variable called ```result``` and output ```result```. \n \
                            4. In principle, one proposition can only correspond to one line of pyDatalog code.\n \
                            5. Do not use any python keywords as variable names. If there is a possible expression in the proposition, such as "round", please use "is_round" instead.\n \
                            6. Dynamically update the variables in ```pyDatalog.create_terms```, add variables that are not mentioned, and delete variables that are not used.\n \
                            The Propositions and Questions are as follows: \n \
                            ```Propositions：\n \
                                Dinner is located in table. \n \
                                Water is located in beer. \n \
                                Inmate is located in house. \n \
                                Water is not located in car show. \n \
                                Water is not located in stuttgart. \n \
                                Water is not located in western hemisphere. \n \
                                Rubber stamp is located in health center. \n \
                                Table is located in house. \n \
                                Beer is located in dinner. \n \
                                Mouse in wall is located in house. \n \
                                Inmate is not located in health center. \n \
                                Water is not located in car show```\n \
                            ```Questions: Water is located in table.```,\n \
                            Your expected output is following, only containing code:\n \
                                import traceback\n \
                                from pyDatalog import pyDatalog\n \
                                try:\n \
                                    pyDatalog.create_terms('X, Y, Z, Located_in, Water, Table, Dinner, Beer, Inmate, House, Car_show, Stuttgart, Western_hemisphere, Rubber_stamp, Health_center, Mouse_in_wall, result, Is_connected')\n \
                                    +Located_in('Dinner', 'Table')\n \
                                    +Located_in('Water', 'Beer')\n \
                                    +Located_in('Inmate', 'House')\n \
                                    +Located_in('Rubber_stamp', 'Health_center')\n \
                                    +Located_in('Table', 'House')\n \
                                    +Located_in('Beer', 'Dinner')\n \
                                    +Located_in('Mouse_in_wall', 'House')\n \
                                    -Located_in('Water', 'Car_show')\n \
                                    -Located_in('Water', 'Stuttgart')\n \
                                    -Located_in('Water', 'Western_hemisphere')\n \
                                    -Located_in('Inmate', 'Health_center')\n \
                                    Is_connected(X,Y) <= Located_in(X,Y)\n \
                                    Is_connected(X,Z) <= Located_in(X,Y) & Is_connected(Y,Z)\n \
                                    query_result = Is_connected('Water', 'Table')\n \
                                    print(1 if query_result.data else 0)\n \
                                except Exception as e:\n \
                                    traceback_info = traceback.format_exc()\n \
                                    print(traceback_info)"""),
    "agent_engineer_neg": remove_spaces("""You are an engineer proficient in pyDatalog programming. I hope you learn the problem-solving process provided below and follow this process to complete new tasks.\n \
                                Task: Please help me translate the following executable pyDatalog code into natural language(Propositions and Questions) , meeting the following requirements: \n \
                                1. Phrases/sentences with the same meaning need to use the same variable name.\n \
                                2. In principle, one proposition can only correspond to one line of pyDatalog code.\n \
                                3. All variable names in python codes are not python keywords.\n \
                                4. Generate only the propositions and questions I want you to generate in the format, do not generate any other content, which includes your introductory words. All I want is the propositions and questions.\n \
                                5. The order of generation must be consistent, that is, the code of the fourth proposition must be ranked fourth in the generated natural language propositions\n \
                                Example:\n \
                                The codes are as follows:\n \
                                import traceback\n \
                                from pyDatalog import pyDatalog\n \
                                try:\n \
                                    pyDatalog.create_terms('X, Y, Z, Located_in, Water, Table, Dinner, Beer, Inmate, House, Car_show, Stuttgart, Western_hemisphere, Rubber_stamp, Health_center, Mouse_in_wall, result, Is_connected')\n \
                                    +Located_in('Dinner', 'Table')\n \
                                    +Located_in('Water', 'Beer')\n \
                                    +Located_in('Inmate', 'House')\n \
                                    +Located_in('Rubber_stamp', 'Health_center')\n \
                                    +Located_in('Table', 'House')\n \
                                    +Located_in('Beer', 'Dinner')\n \
                                    +Located_in('Mouse_in_wall', 'House')\n \
                                    -Located_in('Water', 'Car_show')\n \
                                    -Located_in('Water', 'Stuttgart')\n \
                                    -Located_in('Water', 'Western_hemisphere')\n \
                                    -Located_in('Inmate', 'Health_center')\n \
                                    Is_connected(X,Y) <= Located_in(X,Y)\n \
                                    Is_connected(X,Z) <= Located_in(X,Y) & Is_connected(Y,Z)\n \
                                    query_result = Is_connected('Water', 'Table')\n \
                                    print(1 if query_result.data else 0)\n \
                                except Exception as e:\n \
                                    traceback_info = traceback.format_exc()\n \
                                    print(traceback_info)\n \
                                Your expected output is following, i.e. the Propositions and Questions: \n \
                                ```Propositions：\n \
                                    Dinner is located in table. \n \
                                    Water is located in beer. \n \
                                    Inmate is located in house. \n \
                                    Water is not located in car show. \n \
                                    Water is not located in stuttgart. \n \
                                    Water is not located in western hemisphere. \n \
                                    Rubber stamp is located in health center. \n \
                                    Table is located in house. \n \
                                    Beer is located in dinner. \n \
                                    Mouse in wall is located in house. \n \
                                    Inmate is not located in health center. \n \
                                    Water is not located in car show```\n \
                                ```Questions: Water is located in table.```\n \
    """),
    "no_extra_content": remove_spaces("Your output code will be saved directly into the py file and executed, so anything other than code is prohibited."),
    "adjustment_agent": remove_spaces("""You are an engineer proficient in pyDatalog programming. Please help me fix the code according to the error message provided, and meet the following requirements:\n \
                                            1. Understand the expression of the error message, and modify the code according to the expression, so that the code can correctly output 0/1 instead of abnormal values. \n \
                                            2. Only the pyDatalog code is output, no other explanatory text is included in the response."""),
    "check_error_part1": remove_spaces("""You are a master of linguistics. I hope you compare the following two texts to see if there are any semantic differences. Please follow the following requirements:\n \
                                1. The words themselves must be consistent, rather than considering whether the word meaning is similar. For example, ```huge``` and ```big``` should be regarded as differences.\n \
                                2. The number of propositions in the two texts must be consistent (including propositions and rules), otherwise it will be regarded as a difference.\n \
                                3. If there is a difference, please tell me the difference.\n \
                                Please think about this question step by step. """),
    "check_error_part2": remove_spaces("""Based on your analysis process of text comparison, please give me a final conclusion. We only consider differences in content expression of texts and ignore differences in expression or structure. If there are differences, I hope you will provide me with the specific difference information when summarizing, so that it can help improve the code.
                                        your expected output should be like: \n \
                                        Bob is huge.(original) vs Bob is big.(generated):they are different."""),
    "regeneration": remove_spaces("""I interacted with you and completed the following actions:\n \
                                1. I asked you to help me convert logical reasoning problems described in natural language into pydatalog code.\n \
                                2. After the first step is completed, I asked you to convert the pydatalog code you generated back into a logical reasoning problem described in natural language (note that in this step, I did not provide you with the context of the first step's behavior)\n \
                                3. I asked you to compare the logical reasoning questions in the original natural language form in the first step with the logical reasoning questions in the natural language form converted according to the code in the second step, and asked you to return any possible differences.\n \
                                It is known that the difference you return is as follows:\n \
                                Now please regenerate the pydatalog code for me considering the differences:""")

}