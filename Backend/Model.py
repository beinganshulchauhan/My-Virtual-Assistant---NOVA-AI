# import cohere # import the cohrence library for AI services # content generation
# from rich import print # import the rich library to enhance terminal output
# from dotenv import dotenv_values

# # Load environment variables fron .env files 
# env_vars = dotenv_values(".env")
# CohereAPIkey = env_vars.get("CohereAPIkey")  # Ensure the correct key name

# # Initialize Cohere Client
# co = cohere.Client(api_key=CohereAPIkey)

# # Define a list recognized function keyword for task categorization
# funcs = [
#     "exit", "general", "realtime", "open", "close", "play",
#     "generate image", "system", "content", "google search",
#     "youtube search", "reminder",
#     "message",        # ← ADD
#     "add to cart",    # ← ADD
#     "search and click", # ← ADD
#     "amazon search"
# ]

# # Intialize an empty list to store the user messages
# messages= []

# preamble = """
# You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.
# You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation.
# *** Do not answer any query, just decide what kind of query is given to you. ***

# -> Respond with 'general ( query )' if a query can be answered by a llm model and doesn't require any up to date information like if the query is 'who was akbar?' respond with 'general who was akbar?', if the query is 'how can i study more effectively?' respond with 'general how can i study more effectively?', if the query is 'what is python programming language?' respond with 'general what is python programming language?', if the query is 'Thanks, i really liked it.' respond with 'general thanks, i really liked it.', etc. Respond with 'general (query)' if a query doesn't have a proper noun or is incomplete like 'who is he?', 'what's his networth?', 'tell me more about him.'. Respond with 'general (query)' if the query is asking about time, day, date, month, year like 'what's the time?'.

# -> Respond with 'realtime ( query )' if a query requires up to date or live information that an llm would not know, like:
# - current prices of gold, silver, stocks, crypto, oil, commodities: 'what is gold price today' → 'realtime what is gold price today'
# - current weather: 'what is the weather today' → 'realtime what is the weather today'
# - latest news: 'what is today's news' → 'realtime what is today's news'
# - current sports scores or results: 'who won the match today' → 'realtime who won the match today'
# - recent updates about a person, company, or product: 'tell me about facebook's recent update' → 'realtime tell me about facebook's recent update'
# - who currently holds a position: 'who is indian prime minister' → 'realtime who is indian prime minister'
# - any question with words like 'today', 'current', 'latest', 'now', 'recent', 'live' combined with a factual topic → always realtime
# - who is any living person, YouTuber, celebrity, influencer: 'who is akshay kumar' → 'realtime who is akshay kumar'

# -> Respond with 'open (application name or website name)' if a query is asking to open any application like 'open facebook', 'open telegram', etc.
# -> Respond with 'close (application name)' if a query is asking to close any application like 'close notepad', etc.
# -> Respond with 'play (song name)' if a query is asking to play any song like 'play let her go', etc.
# -> Respond with 'generate image (image prompt)' if a query is requesting to generate an image like 'generate image of a lion', etc.
# -> Respond with 'reminder (datetime with message)' if a query is requesting to set a reminder.
# -> Respond with 'system (task name)' if a query is asking to mute, unmute, volume up, volume down, etc.
# -> Respond with 'content (topic)' if a query is asking to write any content like application, codes, emails, etc.
# -> Respond with 'google search (topic)' if a query is asking to search a specific topic on google.
# -> Respond with 'youtube search (topic)' if a query is asking to search a specific topic on youtube.
# -> Respond with 'message (app name) (contact) (message text)' if the user wants to send a message via an app like 'msg John on whatsapp saying hello' → 'message whatsapp John hello'
# -> Respond with 'add to cart (product name)' if the user wants to add something to Amazon cart like 'add milk to my amazon cart' → 'add to cart milk'
# -> Respond with 'search and click (site) (query)' if the user wants to search something and interact with results.
# "-> Respond with 'amazon search (product)' if the user wants to search something on amazon like 'search football on amazon' respond with 'amazon search football', 'find shoes on amazon' respond with 'amazon search shoes'."

# *** If the query is asking to perform multiple tasks like 'open facebook and close whatsapp' respond with 'open facebook, close whatsapp' ***
# *** If the user is saying goodbye or wants to end the conversation like 'bye nova.' respond with 'exit'. ***
# *** Respond with 'general (query)' if you can't decide the kind of query or if a query is asking to perform a task which is not mentioned above. ***
# """

# # Chat history
# ChatHistory = [
#     {"role": "user", "message": "how are you"},
#     {"role": "Chatbot", "message": "general how are you"},
#     {"role": "user", "message": "what is gold price today"},
#     {"role": "Chatbot", "message": "realtime what is gold price today"},
#     {"role": "user", "message": "what is the weather today"},
#     {"role": "Chatbot", "message": "realtime what is the weather today"},
#     {"role": "user", "message": "what is today's news"},
#     {"role": "Chatbot", "message": "realtime what is today's news"},
#     {"role": "user", "message": "who is the current prime minister of india"},
#     {"role": "Chatbot", "message": "realtime who is the current prime minister of india"},
#     {"role": "user", "message": "who is akshay kumar"},
#     {"role": "Chatbot", "message": "realtime who is akshay kumar"},
#     {"role": "user", "message": "open chrome and tell me about mahatma gandhi"},
#     {"role": "Chatbot", "message": "open chrome, general tell me about mahatma gandhi"},
#     {"role": "user", "message": "what is today's date"},
#     {"role": "Chatbot", "message": "general what is today's date"},
#     {"role": "user", "message": "open spotify and play believer"},
#     {"role": "Chatbot", "message": "open spotify, play believer spotify"},
#     {"role": "user", "message": "play shape of you on spotify"},
#     {"role": "Chatbot", "message": "play shape of you spotify"},
#     {"role": "user", "message": "play despacito on youtube"},
#     {"role": "Chatbot", "message": "play despacito youtube"},
#     {"role": "user", "message": "search football on amazon"},
# {"role": "user", "message": "search football on amazon"},
# {"role": "Chatbot", "message": "amazon search football"},
# {"role": "user", "message": "search iphone on amazon"},
# {"role": "Chatbot", "message": "amazon search iphone"},
# {"role": "user", "message": "find shoes on amazon"},
# {"role": "Chatbot", "message": "amazon search shoes"},
# {"role": "user", "message": "look for headphones on amazon"},
# {"role": "Chatbot", "message": "amazon search headphones"},
# ]

# # Function to interact with Cohere
# def FirstLayerDMM(prompt: str = "test"):
#     # Guard against empty or system messages
#     if not prompt or prompt.strip().lower() in [
#         "no speech detected", "try again", "", "none"
#     ]:
#         return ["general no speech detected"]
    
#     stream = co.chat_stream(
#         model='command-r7b-12-2024',
#         message=prompt,
#         temperature=0.7,
#         chat_history=ChatHistory,  # Ensure correct parameter name
#         prompt_truncation='OFF',
#         connectors=[],
#         preamble=preamble
#     )
    
#     response = ""
#     for event in stream:
#         if event.event_type == "text-generation":  # Fixed comparison operator
#             response += event.text

#     # Clean up response
#     response = response.replace("\n", "").split(",")
#     response = [i.strip() for i in response]  # Trim whitespace

#     # Filter response based on known functions
#     temp = [
#     task for task in response
#     if any(task.startswith(func) for func in funcs)
#     and "(query)" not in task  # ← already exists but double check
#     and "( query )" not in task  # ← spaced version
# ]
    
#     if "(query)" in temp:
#         return FirstLayerDMM(prompt=prompt)  # Recursive call to handle query responses
#     else:
#         return temp


# if __name__ == "__main__":
#     while True:
#         print(FirstLayerDMM(input(">>> ")))



import cohere # import the cohrence library for AI services # content generation
from rich import print # import the rich library to enhance terminal output
from dotenv import dotenv_values

# Load environment variables fron .env files 
env_vars = dotenv_values(".env")
CohereAPIkey = env_vars.get("CohereAPIkey")  # Ensure the correct key name

# Initialize Cohere Client
co = cohere.Client(api_key=CohereAPIkey)

# Define a list recognized function keyword for task categorization
funcs = [
    "exit", "general", "realtime", "open", "close", "play",
    "generate image", "system", "content", "google search",
    "youtube search", "reminder",
    "message",
    "add to cart",
    "search and click",
    "amazon search",
    "open folder",
    "create folder",
    "clipboard"
]

# Intialize an empty list to store the user messages
messages= []

preamble = """
You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.
You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation.
*** Do not answer any query, just decide what kind of query is given to you. ***

-> Respond with 'general ( query )' if a query can be answered by a llm model and doesn't require any up to date information like if the query is 'who was akbar?' respond with 'general who was akbar?', if the query is 'how can i study more effectively?' respond with 'general how can i study more effectively?', if the query is 'what is python programming language?' respond with 'general what is python programming language?', if the query is 'Thanks, i really liked it.' respond with 'general thanks, i really liked it.', etc. Respond with 'general (query)' if a query doesn't have a proper noun or is incomplete like 'who is he?', 'what's his networth?', 'tell me more about him.'. Respond with 'general (query)' if the query is asking about time, day, date, month, year like 'what's the time?'.

-> Respond with 'realtime ( query )' if a query requires up to date or live information that an llm would not know, like:
- current prices of gold, silver, stocks, crypto, oil, commodities: 'what is gold price today' → 'realtime what is gold price today'
- current weather: 'what is the weather today' → 'realtime what is the weather today'
- latest news: 'what is today's news' → 'realtime what is today's news'
- current sports scores or results: 'who won the match today' → 'realtime who won the match today'
- recent updates about a person, company, or product: 'tell me about facebook's recent update' → 'realtime tell me about facebook's recent update'
- who currently holds a position: 'who is indian prime minister' → 'realtime who is indian prime minister'
- any question with words like 'today', 'current', 'latest', 'now', 'recent', 'live' combined with a factual topic → always realtime
- who is any living person, YouTuber, celebrity, influencer: 'who is akshay kumar' → 'realtime who is akshay kumar'

-> Respond with 'open (application name or website name)' if a query is asking to open any application like 'open facebook', 'open telegram', etc.
-> Respond with 'close (application name)' if a query is asking to close any application like 'close notepad', etc.
-> Respond with 'play (song name)' if a query is asking to play any song like 'play let her go', etc.
-> Respond with 'generate image (image prompt)' if a query is requesting to generate an image like 'generate image of a lion', etc.
-> Respond with 'reminder (datetime with message)' if a query is requesting to set a reminder.
-> Respond with 'system (task name)' if a query is asking to mute, unmute, volume up, volume down, etc.
-> Respond with 'content (topic)' if a query is asking to write any content like application, codes, emails, etc.
-> Respond with 'google search (topic)' if a query is asking to search a specific topic on google.
-> Respond with 'youtube search (topic)' if a query is asking to search a specific topic on youtube.
-> Respond with 'message (app name) (contact) (message text)' if the user wants to send a message via an app like 'msg John on whatsapp saying hello' → 'message whatsapp John hello'
-> Respond with 'add to cart (product name)' if the user wants to add something to Amazon cart like 'add milk to my amazon cart' → 'add to cart milk'
-> Respond with 'search and click (site) (query)' if the user wants to search something and interact with results.
-> Respond with 'amazon search (product)' if the user wants to search something on amazon like 'search football on amazon' respond with 'amazon search football', 'find shoes on amazon' respond with 'amazon search shoes'.
-> Respond with 'open folder (folder name)' if the user wants to open a folder like 'open downloads folder' → 'open folder downloads', 'open desktop' → 'open folder desktop', 'open documents' → 'open folder documents'.
-> Respond with 'create folder (name)' if the user wants to create a new folder like 'create a folder named projects' → 'create folder projects'.
-> Respond with 'system screenshot' if the user wants to take a screenshot like 'take a screenshot', 'capture screen'.
-> Respond with 'system lock' if the user wants to lock the computer like 'lock my pc', 'lock screen'.
-> Respond with 'system shutdown' if the user wants to shut down like 'shut down my pc', 'turn off computer'.
-> Respond with 'system restart' if the user wants to restart like 'restart my pc', 'reboot'.
-> Respond with 'system sleep' if the user wants to sleep/hibernate like 'sleep mode', 'put computer to sleep'.
-> Respond with 'system brightness up' if the user wants to increase brightness like 'increase brightness', 'brightness up'.
-> Respond with 'system brightness down' if the user wants to decrease brightness like 'decrease brightness', 'brightness down'.
-> Respond with 'clipboard read' if the user wants to know what's in the clipboard like 'what is in my clipboard', 'read clipboard', 'show clipboard'.
-> Respond with 'clipboard clear' if the user wants to clear the clipboard like 'clear my clipboard', 'empty clipboard'.

*** If the query is asking to perform multiple tasks like 'open facebook and close whatsapp' respond with 'open facebook, close whatsapp' ***
*** If the user is saying goodbye or wants to end the conversation like 'bye nova.' respond with 'exit'. ***
*** Respond with 'general (query)' if you can't decide the kind of query or if a query is asking to perform a task which is not mentioned above. ***
"""

# Chat history
ChatHistory = [
    {"role": "user", "message": "how are you"},
    {"role": "Chatbot", "message": "general how are you"},
    {"role": "user", "message": "what is gold price today"},
    {"role": "Chatbot", "message": "realtime what is gold price today"},
    {"role": "user", "message": "what is the weather today"},
    {"role": "Chatbot", "message": "realtime what is the weather today"},
    {"role": "user", "message": "what is today's news"},
    {"role": "Chatbot", "message": "realtime what is today's news"},
    {"role": "user", "message": "who is the current prime minister of india"},
    {"role": "Chatbot", "message": "realtime who is the current prime minister of india"},
    {"role": "user", "message": "who is akshay kumar"},
    {"role": "Chatbot", "message": "realtime who is akshay kumar"},
    {"role": "user", "message": "open chrome and tell me about mahatma gandhi"},
    {"role": "Chatbot", "message": "open chrome, general tell me about mahatma gandhi"},
    {"role": "user", "message": "what is today's date"},
    {"role": "Chatbot", "message": "general what is today's date"},
    {"role": "user", "message": "open spotify and play believer"},
    {"role": "Chatbot", "message": "open spotify, play believer spotify"},
    {"role": "user", "message": "play shape of you on spotify"},
    {"role": "Chatbot", "message": "play shape of you spotify"},
    {"role": "user", "message": "play despacito on youtube"},
    {"role": "Chatbot", "message": "play despacito youtube"},
    {"role": "user", "message": "search football on amazon"},
{"role": "user", "message": "search football on amazon"},
{"role": "Chatbot", "message": "amazon search football"},
{"role": "user", "message": "search iphone on amazon"},
{"role": "Chatbot", "message": "amazon search iphone"},
{"role": "user", "message": "find shoes on amazon"},
{"role": "Chatbot", "message": "amazon search shoes"},
{"role": "user", "message": "look for headphones on amazon"},
{"role": "Chatbot", "message": "amazon search headphones"},
]

# Function to interact with Cohere
def FirstLayerDMM(prompt: str = "test"):
    # Guard against empty or system messages
    if not prompt or prompt.strip().lower() in [
        "no speech detected", "try again", "", "none"
    ]:
        return ["general no speech detected"]
    
    stream = co.chat_stream(
        model='command-r7b-12-2024',
        message=prompt,
        temperature=0.7,
        chat_history=ChatHistory,  # Ensure correct parameter name
        prompt_truncation='OFF',
        connectors=[],
        preamble=preamble
    )
    
    response = ""
    for event in stream:
        if event.event_type == "text-generation":  # Fixed comparison operator
            response += event.text

    # Clean up response
    response = response.replace("\n", "").split(",")
    response = [i.strip() for i in response]  # Trim whitespace

    # Filter response based on known functions
    temp = [
    task for task in response
    if any(task.startswith(func) for func in funcs)
    and "(query)" not in task  # ← already exists but double check
    and "( query )" not in task  # ← spaced version
]
    
    if "(query)" in temp:
        return FirstLayerDMM(prompt=prompt)  # Recursive call to handle query responses
    else:
        return temp


if __name__ == "__main__":
    while True:
        print(FirstLayerDMM(input(">>> ")))



