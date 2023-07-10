import openai
import os
import templates

# agent_engineer: prompting fot system content
# proposition: prompting for converting all propositions to pyswip code
def ai_function_generation(demo, context, question, requirements, model = "gpt-3.5-turbo"):
    # parse args to comma separated string
    messages = [{"role": "system",
                "content": demo},
                {"role": "user",
                "content": f"Propositions: ```{context}```\nQuestion: ```{question}```, ```{requirements}```"}]

    response = openai.ChatCompletion.create(
        model = model,
        messages = messages,
        temperature = 0
    )

    return response.choices[0].message["content"]