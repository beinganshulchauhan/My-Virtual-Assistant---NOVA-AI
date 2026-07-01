from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options # uses chrome speech reconition model
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt
import time
from selenium.common.exceptions import InvalidSessionIdException


# Load environment variables from the .env file.
env_vars = dotenv_values(".env")

# Get the input language setting from the environment variables
InputLanguage = env_vars.get("InputLanguage")  # Default to English if not set

# Define the HTML code for the speech recognition interface
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript + ' ';
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            if (recognition) {
                recognition.stop();
            }
            output.innerHTML = "";
        }
    </script>
</body>
 </html>'''

HtmlCode = str(HtmlCode).replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

# Create necessary directories if they don’t exist
os.makedirs("Data", exist_ok=True)

# Write the modified HTML code to a file
html_file_path = os.path.join("Data", "Voice.html")
with open(html_file_path, "w", encoding='utf-8') as f:
    f.write(HtmlCode)

# Get the current working directory
current_dir = os.getcwd()

# Generate the file path for the HTML file
Link = os.path.abspath(html_file_path)

# Set Chrome options for Selenium
def CreateDriver():
    chrome_options = Options()

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"

    chrome_options.add_argument(
        f"user-agent={user_agent}"
    )

    chrome_options.add_argument(
        "--use-fake-ui-for-media-stream"
    )
#-------------------------------------------------------------------------------------
   # chrome_options.add_argument("--headless") 

    service = Service(
        ChromeDriverManager().install()
    )

    return webdriver.Chrome(
        service=service,
        options=chrome_options
    )  # Consider removing this if WebRTC does not work properly

# Initialize the Chrome WebDriver
driver = CreateDriver()

# Define the path for temporary files
TempDirPath = os.path.join(current_dir, "Frontend", "Files")
os.makedirs(TempDirPath, exist_ok=True)

# Function to set the assistant's status by writing it to a file
def SetAssistantStatus(Status):
    with open(os.path.join(TempDirPath, "Status.data"), "w", encoding='utf-8') as file:
        file.write(Status)

# Function to modify a query to ensure proper punctuation and formatting
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "which", "whose", "whom", "why", "can you", "what's", "how's"]
    
    if any(word in new_query for word in question_words):
        if query_words and query_words[-1][-1] not in ['.', '?', '!']:
            new_query += "?"
    # else block removed
    return new_query.capitalize()

# Function to translate text into English using mtranslate library
def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

# Function to perform speech recognition using the WebDriver
def SpeechRecognition():

    global driver

    try:
        driver.get("file://" + Link)

    except InvalidSessionIdException:

        print("Browser session lost. Restarting...")

        driver = CreateDriver()

        driver.get("file://" + Link)

    driver.find_element(
        By.ID,
        "start"
    ).click()

    SetAssistantStatus("Listening...")

    start_time = time.time()

    while True:

        try:

            if time.time() - start_time > 10:

                try:
                    driver.find_element(
                        By.ID,
                        "end"
                    ).click()

                except:
                    pass

                SetAssistantStatus(
                    "No speech detected"
                )

                return "No speech detected"

            Text = driver.find_element(
                By.ID,
                "output"
            ).text.strip()

            if Text:

                driver.find_element(
                    By.ID,
                    "end"
                ).click()

                if "en" in InputLanguage.lower():

                    return QueryModifier(Text)

                else:

                    SetAssistantStatus(
                        "Translating..."
                    )

                    return QueryModifier(
                        UniversalTranslator(Text)
                    )

        except Exception as e:

            print(
                f"Recognition Error: {e}"
            )

            driver.quit()

            driver = CreateDriver()

            return "Try again"
# Main execution block
if __name__ == "__main__":
    while True:
        # Continuously perform speech recognition and print the recognized text
        Text = SpeechRecognition()
        print(Text)


    

 