import os
import openai
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_openai_encouragement():
    # TODO: add language
    """A function that will get an encouragement, and
    save that encouragement in crud.py."""

    response = openai.Completion.create(
            model="text-davinci-002",
            prompt=generate_prompt(),
            temperature= 1.0,
            n = 1,
            max_tokens = 250,
        )
    
    return response.choices[0].text.strip()


def generate_prompt():
    return """Brainstorm one encouraging statement for coding students of diverse backgrounds using these examples:
You belong in tech. Push your elbows out and make some room for your seat at the table.
You will be a powerful mentor one day because you understand how hard this road is.
You have learned an unreasonable amount in an impressive amount of time.
Keep up the hard work. One day your code could change someone's life.
Not many people know how hard what you're doing is, but we see you.
"""
    