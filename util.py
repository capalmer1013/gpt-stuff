import os
import time
import json
import datetime

import openai
from github import Github
from rich.console import Console

console = Console()


openai.api_key = os.environ["OPENAI_API_KEY"]
OPENAI_MODEL = os.environ["OPENAI_MODEL"]
GH_ACCESS_TOKEN = os.environ["GH_ACCESS_TOKEN"]
g = Github(GH_ACCESS_TOKEN)

def generate_messages(*args):
    messages = []
    for message in args:
        messages.append({"role": message[0], "content": message[1]})

    return messages


def print_response(response):
    console.print(response, style="green")


def save_response(response, filename):
    with open(filename, "w") as f:
        f.write(response)

class GithubWrapper:
    @staticmethod
    def get_commits(self, username):
        try:
            user = g.get_user(username)
            commits = user.get_commits(since=datetime.datetime.now() - datetime.timedelta(days=7))
            commit_messages = []
            for commit in commits:
                commit_messages.append(commit.commit.message)
        except Exception as e:
            console.print(f"Sorry, This was not possible. Check the error below:\n{e}")
            return

        return commit_messages


class Chat:
    def __init__(self, messages):
        self.messages = messages
        self.completion = None

    def cli(self):
        with open(f"{int(time.time()*100)}.json", "w") as f:
            try:
                while True:
                    print()
                    user_input = input(">>> ")
                    if user_input.lower() == "q":
                        break
                    message = ("user", user_input)
                    self.messages.append(message)
                    self.completion = openai.ChatCompletion.create(
                        model=OPENAI_MODEL,
                        messages=self.messages,
                        temperature=0.7,
                        )

                    message = ("assistant", self.completion.choices[0].message.content)
                    self.messages.append(message)
                    print()
                    console.print("CHAT >", style="color(6)")
                    console.print(self.completion.choices[0].message.content)

            except openai.error.InvalidRequestError as e:
                print(e)
            finally:
                json.dump(self.messages, f)
    
    def single(self):
        self.completion = openai.ChatCompletion.create(model=OPENAI_MODEL, messages=self.messages)
        print_response(self.completion.choices[0].message.content, temperature=0.7)
    
    def edit(self):
        self.completion = openai.Edit.create(
            messages=self.messages,
            model=OPENAI_MODEL,
            temperature=0.7,
        )
        
        return self.completion.choices[0].text
    
    def save_prompt(self, description, filename):
        if input("Save? (y/n): ").lower() == "y":
            save_response(self.completion.choices[0].message.content, filename)
            save_response(description, f"{filename.split('.')[0]}_prompt.txt")
