import os
import openai
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_openai_encouragement(language):
   
    """A function that will get an encouragement, and
    save that encouragement in crud.py."""

    response = openai.Completion.create(
            model="text-davinci-002",
            prompt=generate_prompt(language),
            temperature= 1.0,
            n = 1,
            max_tokens = 250,
        )
    
    return response.choices[0].text.strip()


def generate_prompt(language):

    if language == 'en':
        return """Brainstorm one encouraging statement for coding students of diverse backgrounds using these examples:
You belong in tech. Push your elbows out and make some room for your seat at the table.
You will be a powerful mentor one day because you understand how hard this road is.
You have learned an unreasonable amount in an impressive amount of time.
Keep up the hard work. One day your code could change someone's life.
Not many people know how hard what you're doing is, but we see you.
"""
    if language =='es':
        return """Brainstorm one encouraging statement in Spanish for coding students of diverse backgrounds using these examples:
You are resilient and you can do anything you put your mind to. 
You will be a powerful mentor one day because you understand how hard this road is. 
I'm proud of you for never giving up. You have what it takes to succeed in tech. 
You are brave and determined and you will not let anything stop you from achieving your goals. 
You will make valuable contributions to the coding community.
"""