from googlesearch import search
from groq import Groq               #importing the Groq library to use its API
from json import load, dump         #import functions to read and write JSON files
import datetime                     #importing date and time module for real time date and time information 
from dotenv import dotenv_values    #importing dotenv_values to read environment variables from a .env file



# load environment variables from the .env files
env_vars=dotenv_values(".env")


# Retrieve specific environment variables for username,assistant name,and API key
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIkey = env_vars.get("GroqAPIkey")


# Initialize the Graq client with the provided API key
client = Groq(api_key=GroqAPIkey)

# Define the system instructions for the chatbot
System = f"""
You are {Assistantname}, an intelligent AI assistant for {Username}.

You have real-time internet access. Search results will be provided to you directly in this conversation.
ALWAYS use those search results to answer. NEVER say you lack internet access or real-time information.

Rules:
- Answer directly using the search results provided to you.
- Keep replies under 2-4 sentences unless the user asks for details.
- If search results are available, use them as your primary source.
- Never claim you cannot access the internet or browse the web.
- Never say your knowledge has a cutoff — you have live search results.
- Reply only in English.
- Behave consistently as {Assistantname}.
"""

# Try to load the chat log from a JSON file , or create an empty one if it does not exist
try:
    with open(r"Data\ChatLog.json","r") as f:
        messages = load(f)       # load existing messages from the chat Log
except : 
    # if file does not exist ,create an empty JSON file to store chat logs
    with open(r"Data\ChatLog.json","w")  as f:
        dump([],f)  
# Function to perform a google search and format the results

from tavily import TavilyClient

# Initialize Tavily
TavilyAPIkey = env_vars.get("TavilyAPIkey")
tavily = TavilyClient(api_key=TavilyAPIkey)


def GoogleSearch(query):
    try:
        response = tavily.search(
            query=query,
            search_depth="basic",   # faster
            max_results=5           # less data
        )

        results = response.get("results", [])

        if not results:
            return f"""
The search results for '{query}' are:
[start]
No search results found.
[end]
"""

        Answer = f"The search results for '{query}' are:\n[start]\n"

        for result in results:
            title = result.get("title","")
            content = result.get("content","")

            # trim long content
            content = content[:300]

            Answer += (
                f"Title: {title}\n"
                f"Description: {content}\n\n"
            )

        Answer += "[end]"

        return Answer

    except Exception as e:
        return f"Search Error: {str(e)}"
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer 
 # Predefined chatbot conversation system message and an initial user message
SystemChatBot=[
    {"role":"system","content":System},
    {"role":"user","content":"Hi"},
    {"role":"assistant","content":"Hello, How can I help you?"}
     
 ]
# Function for real time information like current date and time
def Information():
    data=""
    current_date_time = datetime.datetime.now()  # get current date and time
    day = current_date_time.strftime("%A")  # Day of the week
    date =  current_date_time.strftime("%d") # Day of the month
    month =  current_date_time.strftime("%B") # Full month name
    year =  current_date_time.strftime("%Y")  #Year
    hour =  current_date_time.strftime("%H")  # Hour in 24 hour format
    minute =  current_date_time.strftime("%M") # Minute
    second =  current_date_time.strftime("%S") # second
    
    # Format the information into a string
    data = f"Please use this real_time information if needed:\n"
    data += f"Day: {day}\n"
    data += f"Date :{date}\n"
    data +=  f"Month: {month}\n"
    data +=  f"Year: {year}\n"
    data += f"Time: {hour} hours, {minute} minutes ,{second} second.\n"
    return data

# Function to handle real-time search and response generation

def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages

    print(f"DEBUG - Realtime prompt: '{prompt}'")  # ← add
    
    search_result = GoogleSearch(prompt)
    print(f"DEBUG - Search result: {search_result[:200]}")  # ← add

    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)

    messages = messages[-20:]
    messages.append({"role": "user", "content": prompt})
    SystemChatBot.append({"role": "system", "content": search_result})  # ← use variable

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
        max_tokens=512,
        temperature=0.4,
        top_p=1,
        stream=True,
        stop=None
    )

    Answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    print(f"DEBUG - Answer: '{Answer[:200]}'")  # ← add

    Answer = Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})

    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

    SystemChatBot.pop()
    return AnswerModifier(Answer=Answer)
# Main entry point of the program for interactive querying
if __name__ == "__main__":
    while True:
        try:
            prompt = input("Enter your Query: ")
            print(RealtimeSearchEngine(prompt))

        except KeyboardInterrupt:
            print("\nExiting Nova AI safely...")
            break
          
        



