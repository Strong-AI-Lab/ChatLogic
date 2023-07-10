import re

def remove_spaces(text):
    # Replace multiple spaces with a single space
    text = re.sub(r' +', ' ', text)
    # Remove leading and trailing spaces from each line
    text = re.sub(r'^ +| +$', '', text, flags=re.MULTILINE)
    return text

templates = {
    "agent_engineer": remove_spaces("""You are an engineer proficient in PySWIP programming. I hope you learn the problem-solving process provided below and follow this process to complete new tasks.\n \
                            Task: Please help me translate the following natural language(Propositions and Questions) into executable PySWIP code, meeting the following requirements: \n \
                            1. Phrases/sentences with the same meaning need to use the same variable name. \n \
                            2. Only output pyswip code and do not include any other explanatory text in your response. \n \
                            3. Save the judgment result ```(true/false)``` of the question into a variable called ```result``` and output ```result```. \n \
                            The Propositions and Questions are as follows: \n \
                            ```Propositions：\n \
                                Anne is big. \n \
                                big people are nice. \n \
                                All nice people are wealthy. \n \
                                Questions：\n \
                                Anne is wealthy. ``` \n \
                            Your expected output is following, only containing code:\n \
                            ```from pyswip import Prolog \n \
                            prolog = Prolog() \n \
                            # Propositions \n \
                            prolog.assertz("big(anne)") \n \
                            prolog.assertz("nice(X) :- big(X)") \n \
                            prolog.assertz("wealthy(X) :- nice(X)") \n \
                            # Questions \n \
                            query = "wealthy(anne)" \n \
                            results = list(prolog.query(query)) \n \
                            if results: \n \
                                print("true") \n \
                            else: \n \
                                print("false")```"""),
    "no_extra_content": "Your output code will be saved directly into the py file and executed, so anything other than code is prohibited."

}