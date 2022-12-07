import os
import openai
import requests
from helloapp.models import CrazyLibs

# openai.api_key = "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"
openai.api_key = "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"

crazyLibs = CrazyLibs


def generate_crazy_libs():
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
    print(crazyLibs.added_story)

    return crazyLibs


def initiate_story():
    api_url = "https://api.quotable.io/random"
    response = requests.get(api_url)
    crazyLibs.initial_text = response.json()["content"]
    print(crazyLibs.initial_text)
    return crazyLibs.initial_text
