from Frontend.GUI import (
    GraphicalUserInterface,
    SetAssistantStatus,
    ShowTextToScreen,
    TempDirectoryPath,
    SetMicrophoneStatus,
    AnswerModifier,
    QueryModifier,
    GetMicrophoneStatus,
    GetAssistantStatus,
)
from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os
import sys


#-------------------------

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer


def QueryModifier(Query):

    new_query = Query.lower().strip()

    if not new_query:
        return ""

    query_words = new_query.split()

    question_words = [
        "how",
        "what",
        "who",
        "when",
        "why",
        "where",
        "which",
        "whose",
        "whom",
        "can you",
        "what's",
        "where's",
        "how's"
    ]

    if any(word+" " in new_query for word in question_words):

        if query_words[-1][-1] in ['.','?','!']:
            new_query=new_query[:-1]+"?"
        else:
            new_query+="?"

    else:

        if query_words[-1][-1] in ['.','?','!']:
            new_query=new_query[:-1]+"."
        else:
            new_query+="."

    return new_query.capitalize()


def GetMicrophoneStatus():

    path=TempDirectoryPath("Mic.data")

    if not os.path.exists(path):

        with open(path,"w") as f:
            f.write("True")

    with open(path,"r") as f:
        return f.read()


def GetAssistantStatus():

    path=TempDirectoryPath("Status.data")

    if not os.path.exists(path):

        with open(path,"w") as f:
            f.write("Ready")

    with open(path,"r",encoding="utf-8") as f:
        return f.read()
    
    #-----------------------------------------------------------
# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
DefaultMessage = f'''{Username} : Hello {Assistantname}, How are you?
{Assistantname} : Welcome {Username}. I am doing well. How may I help you?'''

# List of supported functions
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

def ShowDefaultChatIfNoChats():
    """Show default chat if no chats exist."""
    with open(r'Data\ChatLog.json', "r", encoding='utf-8') as file:
        if len(file.read()) < 5:
            with open(TempDirectoryPath('Database.data'), "w", encoding='utf-8') as file:
                file.write("")
            with open(TempDirectoryPath('Responses.data'), "w", encoding='utf-8') as file:
                file.write(DefaultMessage)

def ReadChatLogJson():
    """Read and return chat log data from JSON file."""
    with open(r'Data\ChatLog.json', "r", encoding='utf-8') as file:
        chatlog_data = json.load(file)
    return chatlog_data

def ChatLogIntegration():
    """Integrate chat log data into the database."""
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"User: {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"Assistant: {entry['content']}\n"
    formatted_chatlog = formatted_chatlog.replace("User", Username + " ")
    formatted_chatlog = formatted_chatlog.replace("Assistant", Assistantname + " ")
    with open(TempDirectoryPath('Database.data'), "w", encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))

def ShowChatOnGUI():
    """Display chat on the GUI."""
    with open(TempDirectoryPath("Database.data"), "r", encoding='utf-8') as file:
        data = file.read()
    if len(str(data)) > 0:
        lines = data.split('\n')
        result = '\n'.join(lines)
        with open(TempDirectoryPath('Responses.data'), "w", encoding='utf-8') as file:
            file.write(result)

def InitialExecution():
    """Initialize the application."""
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatOnGUI()

# Run initial setup
InitialExecution()

def MainExecution():
    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""

    SetAssistantStatus("Listening....")
    Query = SpeechRecognition()

    print(f"DEBUG - Query: '{Query}'")

    if not Query or Query.strip().lower() in [
        "no speech detected", "try again", "", "none", "goodbye", "bye"
    ]:
        SetAssistantStatus("Available....")
        return False

    ShowTextToScreen(f"{Username} : {Query}")
    SetAssistantStatus("Thinking....")
    Decision = FirstLayerDMM(Query)

    print(f"Decision: {Decision}")  # Debugging: Check what Decision contains

    G = any([i for i in Decision if i.startswith("general")])
    R = any([i for i in Decision if i.startswith("realtime")])

    Merged_query = " and ".join(
        [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
    )

    for queries in Decision:
        if "generate" in queries:
            ImageGenerationQuery = str(queries)
            ImageExecution = True

    for queries in Decision:
        if not TaskExecution:
            if any(queries.startswith(func) for func in Functions):
                run(Automation(list(Decision)))  # passes ALL decisions
                TaskExecution = True # Ensure TaskExecution is set to True after execution

    if ImageExecution and ImageGenerationQuery:
        try:
            # Create necessary directories
            os.makedirs(os.path.join("Frontend", "Files"), exist_ok=True)
            image_data_path = os.path.join("Frontend", "Files", "ImageGeneration.data")
            
            # Write the generation request
            with open(image_data_path, "w", encoding='utf-8') as file:
                file.write(f"{ImageGenerationQuery},True")

            # Get absolute path to image generation script
            image_gen_script = os.path.abspath(os.path.join("Backend", "ImageGeneration.py"))

            # Use correct Python interpreter
            creationflags = 0
            if sys.platform == "win32":
                creationflags = subprocess.CREATE_NO_WINDOW

            process = subprocess.Popen(
                [sys.executable, image_gen_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                shell=False,
                creationflags=creationflags
            )

            stdout, stderr = process.communicate()

            if process.returncode != 0:
                raise Exception(f"Image generation failed: {stderr.decode('utf-8')}")
            
            ShowTextToScreen(f"{Assistantname} : Generating image of {ImageGenerationQuery}...")
            TextToSpeech(f"Generating image of {ImageGenerationQuery}")

        except Exception as e:
            print(f"Error: {str(e)}")
            ShowTextToScreen(f"{Assistantname} : Sorry, I couldn't start the image generation.")
            TextToSpeech("Image generation failed to start")

    if (G and R) or R:
        SetAssistantStatus("Searching....")
        Answer = RealtimeSearchEngine(QueryModifier(Merged_query))
        ShowTextToScreen(f"{Assistantname} : {Answer}")
        SetAssistantStatus("Answering....")
        TextToSpeech(Answer)
        return True
    else:
        for Queries in Decision:
            if "general" in Queries:
                SetAssistantStatus("Thinking....")
                QueryFinal = Queries.replace("general", "")
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname} : {Answer}")
                SetAssistantStatus("Answering....")
                TextToSpeech(Answer)
                return True
            elif "realtime" in Queries:
                SetAssistantStatus("Searching....")
                QueryFinal = Queries.replace("realtime", "")
                Answer = RealtimeSearchEngine(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname} : {Answer}")
                SetAssistantStatus("Answering....")
                TextToSpeech(Answer)
                return True
            elif "exit" in Queries:
                QueryFinal = "Okay, Bye!"
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname} : {Answer}")
                SetAssistantStatus("Answering....")
                TextToSpeech(Answer)
                os._exit(1)

def FirstThread():
    while True:
        CurrentStatus = GetMicrophoneStatus()
        if CurrentStatus == "True":
            SetMicrophoneStatus("False")
            MainExecution()
            sleep(0.5)
            SetMicrophoneStatus("True")  # 👈 Auto re-enable mic after task
        else:
            AIStatus = GetAssistantStatus()
            if "Available...." in AIStatus:
                sleep(0.1)
            else:
                SetAssistantStatus("Available....")

def SecondThread():
    """Second thread for running the GUI."""
    GraphicalUserInterface()

if __name__ == "__main__":
    ai_thread = threading.Thread(target=FirstThread, daemon=True)
    ai_thread.start()

    SecondThread()
