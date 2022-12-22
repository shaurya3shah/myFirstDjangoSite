import os
import openai
import requests

from fun.models.models import CrazyLibs
from myFirstDjangoSite.settings import env

# openai.api_key = "bad1"
# openai.api_key = "bad2"
openai.api_key = env("OPEN_API_KEY")

crazyLibs = CrazyLibs


def generate_original_libs():
    initiate_story()
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=crazyLibs.initial_text,
        temperature=0,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    crazyLibs.added_story = response.choices[0].text
    crazyLibs.crazy_story = ""
    print(crazyLibs.added_story)

    return crazyLibs


def initiate_story():
    api_url = "https://api.quotable.io/random"
    response = requests.get(api_url)
    crazyLibs.initial_text = response.json()["content"]
    print(crazyLibs.initial_text)
    return crazyLibs.initial_text
