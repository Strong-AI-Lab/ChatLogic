import openai
import os


def ai_function(function, args, description, model = "gpt-3.5-turbo"):
    # parse args to comma separated string
    args = ", ".join(args)
    messages = [{"role": "system", "content": f"You are now the following python function: ```# {description}\n{function}```\n\nOnly respond with your `return` value. Do not include any other explanatory text in your response."},{"role": "user", "content": args}]

    response = openai.ChatCompletion.create(
        model = model,
        messages = messages,
        temperature = 0
    )

    return response.choices[0].message["content"]