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
    "no_extra_content": remove_spaces("Your output code will be saved directly into the py file and executed, so anything other than code is prohibited."),
    "adjustment_agent": remove_spaces("""You are an engineer proficient in pyDatalog programming. Please help me fix the code according to the error message provided, and meet the following requirements:\n \
                                            1. Understand the expression of the error message, and modify the code according to the expression, so that the code can correctly output 0/1 instead of abnormal values. \n \
                                            2. Only the pyDatalog code is output, no other explanatory text is included in the response.""")
}