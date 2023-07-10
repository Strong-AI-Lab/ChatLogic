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
                            2. Only output pyswip code and do not include any other explanatory text in your response. \n \
                            3. Save the judgment result ```(1/0)``` of the question into a variable called ```result``` and output ```result```. \n \
                            4. In principle, one proposition can only correspond to one line of pyDatalog code.\n \
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
                                If someone is smart then they are clever. \n \
                                If someone is clever then they are wealthy. \n \
                                If someone is wealthy then they are strong. \n \
                                All strong people are huge.```\n \
                            ```Questions: Fiona is huge.```,\n \
                            Your expected output is following, only containing code:\n \
                            ```from pyDatalog import pyDatalog\n \
                                # Declare the pyDatalog variables\n \
                                pyDatalog.create_terms('X, big, kind, nice, quiet, smart, sad, bad, high, heavy, clever, wealthy, strong, huge')\n \
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
                                clever(X) <= smart(X)\n \
                                wealthy(X) <= clever(X)\n \
                                strong(X) <= wealthy(X)\n \
                                huge(X) <= strong(X)\n \
                                # Query the knowledge base\n \
                                result = huge('Fiona')\n \
                                if result:\n \
                                    print(1)\n \
                                else:\n \
                                    print(0)```"""),
    "no_extra_content": "Your output code will be saved directly into the py file and executed, so anything other than code is prohibited."

}