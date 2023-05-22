import pyttsx3
import webbrowser
import wikipedia
import sys
import time
import datetime
import requests
import json
from num2words import num2words
import openai

# Setting up the OpenAI API credentials
openai.api_key = 'i dont wanna share my api key! go get your own'

# Setting the engine
engine = pyttsx3.init()
engine.setProperty('rate', 100)

# Setting the say function
def say(text):
    encoded_text = text.encode(sys.stdout.encoding, errors='replace')
    decoded_text = encoded_text.decode(sys.stdout.encoding)
    engine.say(decoded_text)
    print(decoded_text)
    engine.runAndWait()

# Setting the function to take the command (tc= take command)
def tc():
    return input("User: ")

# Function to fetch a random joke from an API
def fetch_joke():
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    joke_data = json.loads(response.text)
    joke = joke_data['setup'] + " " + joke_data['punchline']
    return joke

say("Hello, I am Monday! How may I help you?")
while True:
    valid_instruction = False  # Set valid_instruction as False initially
    query = tc()
    sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.org"], ["google", "https://www.google.com"]]

    # Check if the query matches a site to open
    for site in sites:
        if f"Open {site[0]}".lower() in query.lower():
            say(f"Opening {site[0]}...")
            wb.open(site[1])
            valid_instruction = True
    
    # Check if the query is to exit
    if "exit".lower() in query.lower():
        say("Bye sir!")
        valid_instruction = True
        break
    
    # Check if the query is to search on Wikipedia
    elif "search on wikipedia".lower() in query.lower():
        search_on_wiki = query.replace("search on wikipedia", "").strip()
        try:
            wiki = wikipedia.summary(search_on_wiki, sentences=2)
            say(wiki)
        except wikipedia.exceptions.DisambiguationError:
            say("There are multiple results for this query. Please be more specific.")
        except wikipedia.exceptions.PageError:
            say("Sorry, no results found for this query.")
        valid_instruction = True

    # Check if the query is to search on YouTube
    elif "search on youtube".lower() in query.lower():
        search_on_youtube = query.replace("search on youtube", "").strip()
        query_url = "https://www.youtube.com/results?search_query=" + search_on_youtube.replace(" ", "+")
        say("Searching on YouTube...")
        wb.open(query_url)
        valid_instruction = True

    # Check if the query is to perform calculations
    elif "calculate".lower() in query.lower():
        calculation = query.replace("calculate", "").strip()
        try:
            result = eval(calculation)
            say(f"The result is {result}")
        except:
            say("Sorry, I couldn't perform the calculation.")
        valid_instruction = True

    # Check if the query is to fetch a random joke
    elif "tell me a joke".lower() in query.lower():
        joke = fetch_joke()
        say(joke)
        valid_instruction = True

    # Check if the query is to tell the time
    elif "tell me the time".lower() in query.lower():
        current_time = datetime.datetime.now().time()
        hour = num2words(current_time.hour)
        minute = num2words(current_time.minute)
        time_in_words = f"It's {hour} {minute}"
        say(time_in_words)
        valid_instruction = True

    elif "who made you".lower() in query.lower():
        say("I was built by Abhishek Meena! He is very good at coding")
    
    # Chat with OpenAI
    else:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f'Abhishek: {query}\nMonday: ',
            max_tokens=100,
            temperature=1
        )
        reply = response.choices[0].text.strip()
        say(reply)
        valid_instruction = True

    # If the instruction is not valid, prompt the user again
    if not valid_instruction:
        say("Invalid instruction. Please try again.")
