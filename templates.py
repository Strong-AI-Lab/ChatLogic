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
                                Alan is big.\n \
                                Fiona is kind. \n \
                                Fiona is nice. \n \
                                Fiona is quiet. \n \
                                Big people are kind. \n \
                                If someone is kind and nice then they are smart. \n \
                                All sad people are bad. \n \
                                If someone is quiet then they are high. \n \
                                All high people are heavy. \n \
                                If someone is smart then they are round. \n \
                                If someone is round then they are wealthy. \n \
                                If someone is wealthy then they are strong. \n \
                                All strong people are huge.```\n \
                            ```Questions: Fiona is huge.```,\n \
                            Your expected output is following, only containing code:\n \
                            import traceback
                            from pyDatalog import pyDatalog\n \
                                try:     
                                    # Declare the pyDatalog variables\n \
                                    pyDatalog.create_terms('X, big, kind, nice, quiet, smart, sad, bad, high, heavy, is_round, wealthy, strong, huge')\n \
                                    # Define the facts\n \
                                    +big('Alan')\n \
                                    +kind('Fiona')\n \
                                    +nice('Fiona')\n \
                                    +quiet('Fiona')\n \
                                    # Define the rules\n \
                                    kind(X) <= big(X)\n \
                                    smart(X) <= kind(X) & nice(X)\n \
                                    bad(X) <= sad(X)\n \
                                    high(X) <= quiet(X)\n \
                                    heavy(X) <= high(X)\n \
                                    is_round(X) <= smart(X)\n \
                                    wealthy(X) <= is_round(X)\n \
                                    strong(X) <= wealthy(X)\n \
                                    huge(X) <= strong(X)\n \
                                    # Query the knowledge base\n \
                                    result = huge('Fiona')\n \
                                    if result:\n \
                                        print(1)\n \
                                    else:\n \
                                        print(0)
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
                                    # Declare the pyDatalog variables\n \
                                    pyDatalog.create_terms('X, big, kind, nice, quiet, smart, sad, bad, high, heavy, is_round, wealthy, strong, huge')\n \
                                    # Define the facts\n \
                                    +big('Alan')\n \
                                    +kind('Fiona')\n \
                                    +nice('Fiona')\n \
                                    +quiet('Fiona')\n \
                                    # Define the rules\n \
                                    kind(X) <= big(X)\n \
                                    smart(X) <= kind(X) & nice(X)\n \
                                    bad(X) <= sad(X)\n \
                                    high(X) <= quiet(X)\n \
                                    heavy(X) <= high(X)\n \
                                    is_round(X) <= smart(X)\n \
                                    wealthy(X) <= is_round(X)\n \
                                    strong(X) <= wealthy(X)\n \
                                    huge(X) <= strong(X)\n \
                                    # Question\n \
                                    question = +huge('Fiona')\n \
                                except Exception as e:\n \
                                    traceback_info = traceback.format_exc()\n \
                                    print(traceback_info)\n \
                                Your expected output is following, i.e. the Propositions and Questions: \n \
                                ```Propositions:\n \
                                Alan is big.\n \
                                Fiona is kind.\n \
                                Fiona is nice.\n \
                                Fiona is quiet.\n \
                                Big people are kind.\n \
                                If someone is kind and nice then they are smart. All sad people are bad.\n \
                                If someone is quiet then they are high.\n \
                                All high people are heavy.\n \
                                If someone is smart then they are round.\n \
                                If someone is round then they are wealthy. If someone is wealthy then they are strong. All strong people are huge.```\n \
                                ```Questions: Fiona is huge.```\n \
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
    # TODO: need change
    "check_error_part2": remove_spaces("""Based on your analysis process of text comparison, please give me a final conclusion. We only consider differences in content expression of texts and ignore differences in expression or structure. \
                                            If there is no difference between the two texts, please return only the number 1 to me. If there is a difference, please return to me the content of the difference."""),
    "update_code": remove_spaces("""I interacted with you and completed the following actions:\n \
                                1. I asked you to help me convert logical reasoning problems described in natural language into pydatalog code.\n \
                                2. After the first step is completed, I asked you to convert the pydatalog code you generated back into a logical reasoning problem described in natural language (note that in this step, I did not provide you with the context of the first step's behavior)\n \
                                3. I asked you to compare the logical reasoning questions in the original natural language form in the first step with the logical reasoning questions in the natural language form converted according to the code in the second step, and asked you to return any possible differences.\n \
                                It is known that the difference you return is as follows:\n \
                                Now please regenerate the pydatalog code for me considering the differences:"""),
    # TODO: need change
    "regeneration":

}