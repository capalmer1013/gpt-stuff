import openai
import os

# set up OpenAI API credentials
openai.api_key = os.environ["OPENAI_API_KEY"]

# define the prompt for the chatbot
prompt = "Hello, how can I help you today?"

# define the function to interact with the chatbot API
def ask_gpt(prompt):
    # define the parameters for the API request
    params = {
        "engine": "text-davinci-002",
        "prompt": prompt,
        "temperature": 0.7,
        "max_tokens": 1024,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }
    # make the API request and get the response
    response = openai.Completion.create(**params)
    # return the response text
    return response.choices[0].text

# define the main function to interact with the chatbot
def main():
    # start a loop to continuously ask the user for input and output the chatbot's response
    while True:
        # get input from the user
        user_input = input("> ")
        # if the user types "exit", exit the loop and end the program
        if user_input.lower() == "exit":
            break
        # add the user's input to the chatbot prompt
        prompt += "\nUser: " + user_input
        # ask the chatbot for a response based on the updated prompt
        response = ask_gpt(prompt)
        # add the chatbot's response to the prompt
        prompt += "\nChatbot: " + response
        # output the chatbot's response to the user
        print(response)

# run the main function
if __name__ == "__main__":
    main()