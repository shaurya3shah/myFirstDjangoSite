import os
import openai
import requests

openai.api_key = "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"


def generate_crazy_libs():
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=initiate_story(),
        temperature=0,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response


def initiate_story():
    api_url = "https://api.quotable.io/random"
    response = requests.get(api_url)
    initial = response.json()["content"]
    print(initial)
    return initial
