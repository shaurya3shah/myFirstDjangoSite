import os
import openai
import requests
from myFirstDjangoSite.settings import env

openai.api_key = env("OPEN_API_KEY")


def generate_original_libs(initial_text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=initial_text,
        temperature=0,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    added_story = response.choices[0].text
    print(added_story)

    return added_story


def initiate_story():
    api_url = "https://api.quotable.io/random"
    response = requests.get(api_url)
    initial_text = response.json()["content"]
    print(initial_text)
    return initial_text


def generateSentence(word):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="write a single sentence starting with, or containing the word - " + word,
        temperature=0.5,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response)
    return response.choices[0].text


def generatePuzzle(subject):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="can you please give me a " + subject + "  puzzle and solution? And explain the solution",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response)
    return response.choices[0].text


def checkPuzzleAnswer(question, answer):
    prompt = 'for ' + question + ', Answer provided = ' + answer + '. Is the answer provided correct?'
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response)
    return response.choices[0].text
