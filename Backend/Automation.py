# from AppOpener import close, open as appopen
# from webbrowser import open as webopen
# from pywhatkit import playonyt
# from dotenv import dotenv_values
# from bs4 import BeautifulSoup
# from rich import print
# from groq import Groq
# import webbrowser
# import subprocess
# import requests
# import keyboard
# import asyncio
# import os
# from typing import List, Optional, Dict, Any, AsyncGenerator
# from googlesearch import search
# import time
# _open_lock = asyncio.Lock()


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# import urllib.parse


# # Load environmental variables
# env_vars = dotenv_values(".env")
# GroqAPIkey = env_vars.get("GroqAPIkey")

# # CSS classes for parsing HTML content
# CLASSES = [
#     "zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", 
#     "gsrt vk_bk FzvWSb YwPhnf", "pclqee",
#     "tw-Data-text tw-text-small tw-ta", "IZ6rdc",
#     "O5uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table",
#     "dDoNo ikb4Bb gsrt", "sXLaOe", "LWkfKe", "VQF4g",
#     "qv3Wpe", "kno-rdesc", "SPZz6b"
# ]

# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# # Initialize Groq client
# client = Groq(api_key=GroqAPIkey) if GroqAPIkey else None

# PROFESSIONAL_RESPONSES = [
#     "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
#     "I'm at your service for any additional questions or support you may need - don't hesitate to ask."
# ]

# messages: List[Dict[str, str]] = []
# SystemChatBot = [{"role": "system", "content": f"Hello, I am {env_vars.get('Username', 'AI Assistant')}. You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."}]

# def GoogleSearch(topic: str) -> bool:
#     """Perform a Google search using pywhatkit."""
#     try:
#         search(topic)
#         return True
#     except Exception as e:
#         print(f"[red]Error in GoogleSearch: {e}[/red]")
#         return False

# def Content(topic: str) -> bool:
#     """Generate content using AI and save to a file."""
#     def OpenNotepad(file_path: str) -> bool:
#         """Open a file in Notepad."""
#         try:
#             subprocess.Popen(['notepad.exe', file_path])
#             return True
#         except Exception as e:
#             print(f"[red]Error opening Notepad: {e}[/red]")
#             return False

#     def ContentWriterAI(prompt: str) -> str:
#         """Generate content using Groq API."""
#         if not client:
#             raise ValueError("Groq client not initialized")
        
#         messages.append({"role": "user", "content": prompt})
        
#         try:
#             completion = client.chat.completions.create(
#                 model="llama-3.1-8b-instant",
#                 messages=SystemChatBot + messages,
#                 max_tokens=2048,
#                 temperature=0.7,
#                 top_p=1,
#                 stream=True,
#                 stop=None
#             )
            
#             answer = ""
#             for chunk in completion:
#                 if chunk.choices[0].delta.content:
#                     answer += chunk.choices[0].delta.content
            
#             answer = answer.replace("</s>", "")
#             messages.append({"role": "assistant", "content": answer})
#             return answer
#         except Exception as e:
#             print(f"[red]Error in ContentWriterAI: {e}[/red]")
#             raise

#     try:
#         clean_topic = topic.replace("Content", "").strip()
#         content = ContentWriterAI(clean_topic)
        
#         # Ensure Data directory exists
#         os.makedirs("Data", exist_ok=True)
        
#         filename = f"Data/{clean_topic.lower().replace(' ', '_')}.txt"
#         with open(filename, "w", encoding="utf-8") as file:
#             file.write(content)
        
#         OpenNotepad(filename)
#         return True
#     except Exception as e:
#         print(f"[red]Error in Content: {e}[/red]")
#         return False
    
# #------------------------------------------------------------------
# def SendWhatsAppMessage(contact: str, message: str) -> bool:
#     """Open WhatsApp Web and send a message to a contact."""
#     try:
#         encoded_msg = urllib.parse.quote(message)
#         # Search contact by name on WhatsApp Web
#         options = Options()
#         options.add_argument("--user-data-dir=./whatsapp_session")  # saves login session
#         driver = webdriver.Chrome(
#             service=Service(ChromeDriverManager().install()),
#             options=options
#         )

#         driver.get("https://web.whatsapp.com")
#         print("Waiting for WhatsApp Web to load (scan QR if first time)...")
#         time.sleep(8)  # give time to load / scan QR on first run

#         # Search for contact
#         search_box = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
#             )
#         )
#         search_box.click()
#         search_box.send_keys(contact)
#         time.sleep(2)

#         # Click the first matching contact
#         contact_result = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, f'//span[@title="{contact}"]')
#             )
#         )
#         contact_result.click()
#         time.sleep(1)

#         # Type and send the message
#         msg_box = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
#             )
#         )
#         msg_box.click()
#         msg_box.send_keys(message)
#         time.sleep(0.5)
#         msg_box.send_keys("\n")  # press Enter to send

#         time.sleep(2)
#         print(f"Message sent to {contact}!")
#         driver.quit()
#         return True

#     except Exception as e:
#         print(f"[red]Error in SendWhatsAppMessage: {e}[/red]")
#         return False


# def AddToAmazonCart(product: str) -> bool:
#     """Search Amazon for a product and add the first result to cart."""
#     try:
#         options = Options()
#         options.add_argument("--user-data-dir=./amazon_session")  # saves login session
#         driver = webdriver.Chrome(
#             service=Service(ChromeDriverManager().install()),
#             options=options
#         )

#         encoded = urllib.parse.quote(product)
#         driver.get(f"https://www.amazon.in/s?k={encoded}")
#         time.sleep(3)

#         # Click first product
#         first_product = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, '(//div[@data-component-type="s-search-result"]//h2/a)[1]')
#             )
#         )
#         first_product.click()
#         time.sleep(3)

#         # Click Add to Cart
#         add_to_cart_btn = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located(
#                 (By.ID, "add-to-cart-button")
#             )
#         )
#         add_to_cart_btn.click()
#         time.sleep(2)

#         print(f"'{product}' added to Amazon cart!")
#         # Leave browser open so user can see/confirm
#         return True

#     except Exception as e:
#         print(f"[red]Error in AddToAmazonCart: {e}[/red]")
#         return False
    

# #-----------------------------------------------------------------------------------------------


# def YouTubeSearch(topic: str) -> bool:
#     """Search for a topic on YouTube."""
#     try:
#         url = f"https://www.youtube.com/results?search_query={topic}"
#         webbrowser.open(url)
#         return True
#     except Exception as e:
#         print(f"[red]Error in YouTubeSearch: {e}[/red]")
#         return False

# def PlayYoutube(query: str) -> bool:
#     """Play a YouTube video."""
#     try:
#         playonyt(query)
#         return True
#     except Exception as e:
#         print(f"[red]Error in PlayYoutube: {e}[/red]")
#         return False

# def search_google(query):
#     try:
#         results = list(
#             search(
#                 query,
#                 num_results=5
#             )
#         )

#         if results:
#             return results[0]

#         return None

#     except Exception as e:
#         print(f"Search Error: {e}")
#         return None


# async def OpenAppAsync(app):
#     async with _open_lock:  # Only one open at a time
#         if not app or not isinstance(app, str):
#             return False

#         app = app.lower().strip()

#         websites = {
#             "youtube": "https://youtube.com",
#             "google": "https://google.com",
#             "instagram": "https://instagram.com",
#             "facebook": "https://facebook.com",
#             "twitter": "https://twitter.com",
#             "github": "https://github.com"
#         }

#         if app in websites:
#             webopen(websites[app])
#             await asyncio.sleep(2)  # Wait between opens
#             return True

#         if "." in app and " " not in app:
#             webopen("https://" + app)
#             await asyncio.sleep(2)
#             return True

#         try:
#             appopen(app, match_closest=True, output=False, throw_error=True)
#             await asyncio.sleep(1)
#             return True
#         except Exception as e:
#             print(f"App not found: {e}")
#             try:
#                 link = search_google(app)
#                 if link:
#                     webopen(link)
#                     await asyncio.sleep(2)
#                     return True
#             except Exception as e:
#                 print(f"Search failed: {e}")
#             return False

# def CloseApp(app: str) -> bool:
#     """Close an application."""
#     if "chrome" in app.lower():
#         return False
        
#     try:
#         close(app, match_closest=True, output=False, throw_error=True)
#         return True
#     except Exception as e:
#         print(f"[yellow]Warning in CloseApp: {e}[/yellow]")
#         return False
    
# #-------------------------------------------
# def PlaySong(query: str) -> bool:
#     """Play a song - on Spotify if mentioned, else YouTube."""
#     query_lower = query.lower()
    
#     # If spotify is in the query, open spotify and search there
#     if "spotify" in query_lower:
#         song = query_lower.replace("spotify", "").strip()
#         url = f"https://open.spotify.com/search/{song.replace(' ', '%20')}"
#         webopen(url)
#         return True
#     else:
#         # Default: play on YouTube
#         try:
#             playonyt(query)
#             return True
#         except Exception as e:
#             print(f"[red]Error in PlaySong: {e}[/red]")
#             return False    
        
# def AmazonSearch(query: str) -> bool:
#     """Search for a product on Amazon."""
#     try:
#         encoded = urllib.parse.quote(query)
#         webopen(f"https://www.amazon.in/s?k={encoded}")
#         return True
#     except Exception as e:
#         print(f"[red]Error in AmazonSearch: {e}[/red]")
#         return False        

# def System(command: str) -> bool:
#     """Execute system commands."""
#     command = command.lower().strip()
    
#     key_commands = {
#         "mute": "volume mute",
#         "unmute": "volume mute",
#         "volume up": "volume up",
#         "volume down": "volume down"
#     }
    
#     if command in key_commands:
#         try:
#             keyboard.press_and_release(key_commands[command])
#             return True
#         except Exception as e:
#             print(f"[red]Error in System command: {e}[/red]")
#             return False
#     else:
#         print(f"[yellow]Unknown system command: {command}[/yellow]")
#         return False

# async def TranslateAndExecute(commands: List[str]) -> AsyncGenerator[Any, None]:
#     """Translate and execute commands asynchronously."""
#     funcs = []
    
#     for command in commands:
#         command = command.strip().rstrip('.?!')  # safety net
#         if not command:
#             continue
                
#         try:
#             if command.startswith("open "):
#                 if "open it" in command or "open file" in command:
#                     continue
#                 app_name = command.removeprefix("open").strip()
#                 funcs.append(OpenAppAsync(app_name))


#             #---------------------------------------------
#             elif command.startswith("message "):
#                 # Expected format: "message whatsapp John hello how are you"
#                 parts = command.removeprefix("message").strip().split(" ", 2)
#                 if len(parts) >= 3:
#                     app, contact, msg_text = parts[0], parts[1], parts[2]
#                     if "whatsapp" in app.lower():
#                         funcs.append(asyncio.to_thread(SendWhatsAppMessage, contact, msg_text))
#                     else:
#                         print(f"[yellow]Messaging not supported for: {app}[/yellow]")
#                 else:
#                     print(f"[yellow]Not enough info to send message: {command}[/yellow]")

#             elif command.startswith("add to cart "):
#                 product = command.removeprefix("add to cart").strip()
#                 funcs.append(asyncio.to_thread(AddToAmazonCart, product))
            
# #----------------------------------------------------------------------------------------------------

#             elif command.startswith("close "):
#                 app_name = command.removeprefix("close").strip()
#                 funcs.append(asyncio.to_thread(CloseApp, app_name))
                
#             elif command.startswith("play "):
#                 query = command.removeprefix("play").strip()
#                 funcs.append(asyncio.to_thread(PlaySong, query))  # ← was PlayYoutube
                
#             elif command.startswith("content "):
#                 topic = command.removeprefix("content").strip()
#                 funcs.append(asyncio.to_thread(Content, topic))
                
#             elif command.startswith("google search "):
#                 query = command.removeprefix("google search").strip()
#                 funcs.append(asyncio.to_thread(GoogleSearch, query))

#             elif command.startswith("amazon search "):
#                 query = command.removeprefix("amazon search").strip()
#                 funcs.append(asyncio.to_thread(AmazonSearch, query))    
                
#             elif command.startswith("system "):
#                 sys_command = command.removeprefix("system").strip()
#                 funcs.append(asyncio.to_thread(System, sys_command))

#             elif command.startswith("youtube search "):
#                 query = command.removeprefix("youtube search").strip()
#                 funcs.append(asyncio.to_thread(YouTubeSearch, query))    
                            
#             else:
#                 print(f"[yellow]No handler for command: {command}[/yellow]")
                
#         except Exception as e:
#             print(f"[red]Error processing command {command}: {e}[/red]")
    
#     if funcs:
#         try:
#             results = await asyncio.gather(*funcs, return_exceptions=True)
#             for result in results:
#                 if isinstance(result, Exception):
#                     print(f"[red]Command execution error: {result}[/red]")
#                 else:
#                     yield result
#         except Exception as e:
#             print(f"[red]Error in command execution: {e}[/red]")

# async def Automation(commands: List[str]) -> bool:
#     """Automate command execution."""
#     try:
#         async for _ in TranslateAndExecute(commands):
#             pass
#         return True
#     except Exception as e:
#         print(f"[red]Error in Automation: {e}[/red]")
#         return False

# from AppOpener import close, open as appopen
# from webbrowser import open as webopen
# from pywhatkit import playonyt
# from dotenv import dotenv_values
# from bs4 import BeautifulSoup
# from rich import print
# from groq import Groq
# import webbrowser
# import subprocess
# import requests
# import keyboard
# import asyncio
# import os
# from typing import List, Optional, Dict, Any, AsyncGenerator
# from googlesearch import search
# import time


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# import urllib.parse


# # Load environmental variables
# env_vars = dotenv_values(".env")
# GroqAPIkey = env_vars.get("GroqAPIkey")

# # CSS classes for parsing HTML content
# CLASSES = [
#     "zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", 
#     "gsrt vk_bk FzvWSb YwPhnf", "pclqee",
#     "tw-Data-text tw-text-small tw-ta", "IZ6rdc",
#     "O5uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table",
#     "dDoNo ikb4Bb gsrt", "sXLaOe", "LWkfKe", "VQF4g",
#     "qv3Wpe", "kno-rdesc", "SPZz6b"
# ]

# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# # Initialize Groq client
# client = Groq(api_key=GroqAPIkey) if GroqAPIkey else None

# PROFESSIONAL_RESPONSES = [
#     "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
#     "I'm at your service for any additional questions or support you may need - don't hesitate to ask."
# ]

# messages: List[Dict[str, str]] = []
# SystemChatBot = [{"role": "system", "content": f"Hello, I am {env_vars.get('Username', 'AI Assistant')}. You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."}]

# def GoogleSearch(topic: str) -> bool:
#     """Perform a Google search using pywhatkit."""
#     try:
#         search(topic)
#         return True
#     except Exception as e:
#         print(f"[red]Error in GoogleSearch: {e}[/red]")
#         return False

# def Content(topic: str) -> bool:
#     """Generate content using AI and save to a file."""
#     def OpenNotepad(file_path: str) -> bool:
#         """Open a file in Notepad."""
#         try:
#             subprocess.Popen(['notepad.exe', file_path])
#             return True
#         except Exception as e:
#             print(f"[red]Error opening Notepad: {e}[/red]")
#             return False

#     def ContentWriterAI(prompt: str) -> str:
#         """Generate content using Groq API."""
#         if not client:
#             raise ValueError("Groq client not initialized")
        
#         messages.append({"role": "user", "content": prompt})
        
#         try:
#             completion = client.chat.completions.create(
#                 model="llama-3.1-8b-instant",
#                 messages=SystemChatBot + messages,
#                 max_tokens=2048,
#                 temperature=0.7,
#                 top_p=1,
#                 stream=True,
#                 stop=None
#             )
            
#             answer = ""
#             for chunk in completion:
#                 if chunk.choices[0].delta.content:
#                     answer += chunk.choices[0].delta.content
            
#             answer = answer.replace("</s>", "")
#             messages.append({"role": "assistant", "content": answer})
#             return answer
#         except Exception as e:
#             print(f"[red]Error in ContentWriterAI: {e}[/red]")
#             raise

#     try:
#         clean_topic = topic.replace("Content", "").strip()
#         content = ContentWriterAI(clean_topic)
        
#         # Ensure Data directory exists
#         os.makedirs("Data", exist_ok=True)
        
#         filename = f"Data/{clean_topic.lower().replace(' ', '_')}.txt"
#         with open(filename, "w", encoding="utf-8") as file:
#             file.write(content)
        
#         OpenNotepad(filename)
#         return True
#     except Exception as e:
#         print(f"[red]Error in Content: {e}[/red]")
#         return False
    
# #------------------------------------------------------------------
# def SendWhatsAppMessage(contact: str, message: str) -> bool:
#     """Open WhatsApp Web and send a message to a contact."""
#     try:
#         encoded_msg = urllib.parse.quote(message)
#         # Search contact by name on WhatsApp Web
#         options = Options()
#         options.add_argument("--user-data-dir=./whatsapp_session")  # saves login session
#         driver = webdriver.Chrome(
#             service=Service(ChromeDriverManager().install()),
#             options=options
#         )

#         driver.get("https://web.whatsapp.com")
#         print("Waiting for WhatsApp Web to load (scan QR if first time)...")
#         time.sleep(8)  # give time to load / scan QR on first run

#         # Search for contact
#         search_box = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
#             )
#         )
#         search_box.click()
#         search_box.send_keys(contact)
#         time.sleep(2)

#         # Click the first matching contact
#         contact_result = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, f'//span[@title="{contact}"]')
#             )
#         )
#         contact_result.click()
#         time.sleep(1)

#         # Type and send the message
#         msg_box = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
#             )
#         )
#         msg_box.click()
#         msg_box.send_keys(message)
#         time.sleep(0.5)
#         msg_box.send_keys("\n")  # press Enter to send

#         time.sleep(2)
#         print(f"Message sent to {contact}!")
#         driver.quit()
#         return True

#     except Exception as e:
#         print(f"[red]Error in SendWhatsAppMessage: {e}[/red]")
#         return False


# def AddToAmazonCart(product: str) -> bool:
#     """Search Amazon for a product and add the first result to cart."""
#     try:
#         options = Options()
#         options.add_argument("--user-data-dir=./amazon_session")  # saves login session
#         driver = webdriver.Chrome(
#             service=Service(ChromeDriverManager().install()),
#             options=options
#         )

#         encoded = urllib.parse.quote(product)
#         driver.get(f"https://www.amazon.in/s?k={encoded}")
#         time.sleep(3)

#         # Click first product
#         first_product = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, '(//div[@data-component-type="s-search-result"]//h2/a)[1]')
#             )
#         )
#         first_product.click()
#         time.sleep(3)

#         # Click Add to Cart
#         add_to_cart_btn = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located(
#                 (By.ID, "add-to-cart-button")
#             )
#         )
#         add_to_cart_btn.click()
#         time.sleep(2)

#         print(f"'{product}' added to Amazon cart!")
#         # Leave browser open so user can see/confirm
#         return True

#     except Exception as e:
#         print(f"[red]Error in AddToAmazonCart: {e}[/red]")
#         return False
    

# #-----------------------------------------------------------------------------------------------


# def YouTubeSearch(topic: str) -> bool:
#     """Search for a topic on YouTube."""
#     try:
#         url = f"https://www.youtube.com/results?search_query={topic}"
#         webbrowser.open(url)
#         return True
#     except Exception as e:
#         print(f"[red]Error in YouTubeSearch: {e}[/red]")
#         return False

# def PlayYoutube(query: str) -> bool:
#     """Play a YouTube video."""
#     try:
#         playonyt(query)
#         return True
#     except Exception as e:
#         print(f"[red]Error in PlayYoutube: {e}[/red]")
#         return False

# def search_google(query):
#     try:
#         results = list(
#             search(
#                 query,
#                 num_results=5
#             )
#         )

#         if results:
#             return results[0]

#         return None

#     except Exception as e:
#         print(f"Search Error: {e}")
#         return None


# async def OpenAppAsync(app):
#     if not app or not isinstance(app, str):
#         return False

#     app = app.lower().strip()

#     websites = {
#         "youtube": "https://youtube.com",
#         "google": "https://google.com",
#         "instagram": "https://instagram.com",
#         "facebook": "https://facebook.com",
#         "twitter": "https://twitter.com",
#         "github": "https://github.com"
#     }

#     if app in websites:
#         webopen(websites[app])
#         return True

#     if "." in app and " " not in app:
#         webopen("https://" + app)
#         return True

#     try:
#         appopen(app, match_closest=True, output=False, throw_error=True)
#         return True
#     except Exception as e:
#         print(f"App not found: {e}")
#         try:
#             link = search_google(app)
#             if link:
#                 webopen(link)
#                 return True
#         except Exception as e:
#             print(f"Search failed: {e}")
#         return False

# def CloseApp(app: str) -> bool:
#     """Close an application."""
#     if "chrome" in app.lower():
#         return False
        
#     try:
#         close(app, match_closest=True, output=False, throw_error=True)
#         return True
#     except Exception as e:
#         print(f"[yellow]Warning in CloseApp: {e}[/yellow]")
#         return False
    
# #-------------------------------------------
# def PlaySong(query: str) -> bool:
#     """Play a song - on Spotify if mentioned, else YouTube."""
#     query_lower = query.lower()
    
#     # If spotify is in the query, open spotify and search there
#     if "spotify" in query_lower:
#         song = query_lower.replace("spotify", "").strip()
#         url = f"https://open.spotify.com/search/{song.replace(' ', '%20')}"
#         webopen(url)
#         return True
#     else:
#         # Default: play on YouTube
#         try:
#             playonyt(query)
#             return True
#         except Exception as e:
#             print(f"[red]Error in PlaySong: {e}[/red]")
#             return False    
        
# def AmazonSearch(query: str) -> bool:
#     """Search for a product on Amazon."""
#     try:
#         encoded = urllib.parse.quote(query)
#         webopen(f"https://www.amazon.in/s?k={encoded}")
#         return True
#     except Exception as e:
#         print(f"[red]Error in AmazonSearch: {e}[/red]")
#         return False        

# def System(command: str) -> bool:
#     """Execute system commands."""
#     command = command.lower().strip()
    
#     key_commands = {
#         "mute": "volume mute",
#         "unmute": "volume mute",
#         "volume up": "volume up",
#         "volume down": "volume down"
#     }
    
#     if command in key_commands:
#         try:
#             keyboard.press_and_release(key_commands[command])
#             return True
#         except Exception as e:
#             print(f"[red]Error in System command: {e}[/red]")
#             return False
#     else:
#         print(f"[yellow]Unknown system command: {command}[/yellow]")
#         return False

# async def TranslateAndExecute(commands: List[str]) -> AsyncGenerator[Any, None]:
#     """Translate and execute commands asynchronously."""
#     funcs = []
    
#     for command in commands:
#         command = command.strip().rstrip('.?!')  # safety net
#         if not command:
#             continue
                
#         try:
#             if command.startswith("open "):
#                 if "open it" in command or "open file" in command:
#                     continue
#                 app_name = command.removeprefix("open").strip()
#                 funcs.append(OpenAppAsync(app_name))


#             #---------------------------------------------
#             elif command.startswith("message "):
#                 # Expected format: "message whatsapp John hello how are you"
#                 parts = command.removeprefix("message").strip().split(" ", 2)
#                 if len(parts) >= 3:
#                     app, contact, msg_text = parts[0], parts[1], parts[2]
#                     if "whatsapp" in app.lower():
#                         funcs.append(asyncio.to_thread(SendWhatsAppMessage, contact, msg_text))
#                     else:
#                         print(f"[yellow]Messaging not supported for: {app}[/yellow]")
#                 else:
#                     print(f"[yellow]Not enough info to send message: {command}[/yellow]")

#             elif command.startswith("add to cart "):
#                 product = command.removeprefix("add to cart").strip()
#                 funcs.append(asyncio.to_thread(AddToAmazonCart, product))
            
# #----------------------------------------------------------------------------------------------------

#             elif command.startswith("close "):
#                 app_name = command.removeprefix("close").strip()
#                 funcs.append(asyncio.to_thread(CloseApp, app_name))
                
#             elif command.startswith("play "):
#                 query = command.removeprefix("play").strip()
#                 funcs.append(asyncio.to_thread(PlaySong, query))  # ← was PlayYoutube
                
#             elif command.startswith("content "):
#                 topic = command.removeprefix("content").strip()
#                 funcs.append(asyncio.to_thread(Content, topic))
                
#             elif command.startswith("google search "):
#                 query = command.removeprefix("google search").strip()
#                 funcs.append(asyncio.to_thread(GoogleSearch, query))

#             elif command.startswith("amazon search "):
#                 query = command.removeprefix("amazon search").strip()
#                 funcs.append(asyncio.to_thread(AmazonSearch, query))    
                
#             elif command.startswith("system "):
#                 sys_command = command.removeprefix("system").strip()
#                 funcs.append(asyncio.to_thread(System, sys_command))

#             elif command.startswith("youtube search "):
#                 query = command.removeprefix("youtube search").strip()
#                 funcs.append(asyncio.to_thread(YouTubeSearch, query))    
                            
#             else:
#                 print(f"[yellow]No handler for command: {command}[/yellow]")
                
#         except Exception as e:
#             print(f"[red]Error processing command {command}: {e}[/red]")
    
#     if funcs:
#         try:
#             results = await asyncio.gather(*funcs, return_exceptions=True)
#             for result in results:
#                 if isinstance(result, Exception):
#                     print(f"[red]Command execution error: {result}[/red]")
#                 else:
#                     yield result
#         except Exception as e:
#             print(f"[red]Error in command execution: {e}[/red]")

# async def Automation(commands: List[str]) -> bool:
#     """Automate command execution."""
#     try:
#         async for _ in TranslateAndExecute(commands):
#             pass
#         return True
#     except Exception as e:
#         print(f"[red]Error in Automation: {e}[/red]")
#         return False







from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os
from typing import List, Optional, Dict, Any, AsyncGenerator
from googlesearch import search
import time


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import urllib.parse


# Load environmental variables
env_vars = dotenv_values(".env")
GroqAPIkey = env_vars.get("GroqAPIkey")

# CSS classes for parsing HTML content
CLASSES = [
    "zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", 
    "gsrt vk_bk FzvWSb YwPhnf", "pclqee",
    "tw-Data-text tw-text-small tw-ta", "IZ6rdc",
    "O5uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table",
    "dDoNo ikb4Bb gsrt", "sXLaOe", "LWkfKe", "VQF4g",
    "qv3Wpe", "kno-rdesc", "SPZz6b"
]

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# Initialize Groq client
client = Groq(api_key=GroqAPIkey) if GroqAPIkey else None

PROFESSIONAL_RESPONSES = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need - don't hesitate to ask."
]

messages: List[Dict[str, str]] = []
SystemChatBot = [{"role": "system", "content": f"Hello, I am {env_vars.get('Username', 'AI Assistant')}. You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."}]

def GoogleSearch(topic: str) -> bool:
    """Perform a Google search using pywhatkit."""
    try:
        search(topic)
        return True
    except Exception as e:
        print(f"[red]Error in GoogleSearch: {e}[/red]")
        return False

def Content(topic: str) -> bool:
    """Generate content using AI and save to a file."""
    def OpenNotepad(file_path: str) -> bool:
        """Open a file in Notepad."""
        try:
            subprocess.Popen(['notepad.exe', file_path])
            return True
        except Exception as e:
            print(f"[red]Error opening Notepad: {e}[/red]")
            return False

    def ContentWriterAI(prompt: str) -> str:
        """Generate content using Groq API."""
        if not client:
            raise ValueError("Groq client not initialized")
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=SystemChatBot + messages,
                max_tokens=2048,
                temperature=0.7,
                top_p=1,
                stream=True,
                stop=None
            )
            
            answer = ""
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    answer += chunk.choices[0].delta.content
            
            answer = answer.replace("</s>", "")
            messages.append({"role": "assistant", "content": answer})
            return answer
        except Exception as e:
            print(f"[red]Error in ContentWriterAI: {e}[/red]")
            raise

    try:
        clean_topic = topic.replace("Content", "").strip()
        content = ContentWriterAI(clean_topic)
        
        # Ensure Data directory exists
        os.makedirs("Data", exist_ok=True)
        
        filename = f"Data/{clean_topic.lower().replace(' ', '_')}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
        
        OpenNotepad(filename)
        return True
    except Exception as e:
        print(f"[red]Error in Content: {e}[/red]")
        return False
    
#------------------------------------------------------------------
def SendWhatsAppMessage(contact: str, message: str) -> bool:
    """Open WhatsApp Web and send a message to a contact."""
    try:
        encoded_msg = urllib.parse.quote(message)
        # Search contact by name on WhatsApp Web
        options = Options()
        options.add_argument("--user-data-dir=./whatsapp_session")  # saves login session
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        driver.get("https://web.whatsapp.com")
        print("Waiting for WhatsApp Web to load (scan QR if first time)...")
        time.sleep(8)  # give time to load / scan QR on first run

        # Search for contact
        search_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
            )
        )
        search_box.click()
        search_box.send_keys(contact)
        time.sleep(2)

        # Click the first matching contact
        contact_result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, f'//span[@title="{contact}"]')
            )
        )
        contact_result.click()
        time.sleep(1)

        # Type and send the message
        msg_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
            )
        )
        msg_box.click()
        msg_box.send_keys(message)
        time.sleep(0.5)
        msg_box.send_keys("\n")  # press Enter to send

        time.sleep(2)
        print(f"Message sent to {contact}!")
        driver.quit()
        return True

    except Exception as e:
        print(f"[red]Error in SendWhatsAppMessage: {e}[/red]")
        return False


def AddToAmazonCart(product: str) -> bool:
    """Search Amazon for a product and add the first result to cart."""
    try:
        options = Options()
        options.add_argument("--user-data-dir=./amazon_session")  # saves login session
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        encoded = urllib.parse.quote(product)
        driver.get(f"https://www.amazon.in/s?k={encoded}")
        time.sleep(3)

        # Click first product
        first_product = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '(//div[@data-component-type="s-search-result"]//h2/a)[1]')
            )
        )
        first_product.click()
        time.sleep(3)

        # Click Add to Cart
        add_to_cart_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, "add-to-cart-button")
            )
        )
        add_to_cart_btn.click()
        time.sleep(2)

        print(f"'{product}' added to Amazon cart!")
        # Leave browser open so user can see/confirm
        return True

    except Exception as e:
        print(f"[red]Error in AddToAmazonCart: {e}[/red]")
        return False
    

#-----------------------------------------------------------------------------------------------


def YouTubeSearch(topic: str) -> bool:
    """Search for a topic on YouTube."""
    try:
        url = f"https://www.youtube.com/results?search_query={topic}"
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"[red]Error in YouTubeSearch: {e}[/red]")
        return False

def PlayYoutube(query: str) -> bool:
    """Play a YouTube video."""
    try:
        playonyt(query)
        return True
    except Exception as e:
        print(f"[red]Error in PlayYoutube: {e}[/red]")
        return False

def search_google(query):
    try:
        results = list(
            search(
                query,
                num_results=5
            )
        )

        if results:
            return results[0]

        return None

    except Exception as e:
        print(f"Search Error: {e}")
        return None


async def OpenAppAsync(app):
    if not app or not isinstance(app, str):
        return False

    app = app.lower().strip()

    websites = {
        "youtube": "https://youtube.com",
        "google": "https://google.com",
        "instagram": "https://instagram.com",
        "facebook": "https://facebook.com",
        "twitter": "https://twitter.com",
        "github": "https://github.com"
    }

    if app in websites:
        webopen(websites[app])
        return True

    if "." in app and " " not in app:
        webopen("https://" + app)
        return True

    try:
        appopen(app, match_closest=True, output=False, throw_error=True)
        return True
    except Exception as e:
        print(f"App not found: {e}")
        try:
            link = search_google(app)
            if link:
                webopen(link)
                return True
        except Exception as e:
            print(f"Search failed: {e}")
        return False

def CloseApp(app: str) -> bool:
    """Close an application."""
    if "chrome" in app.lower():
        return False
        
    try:
        close(app, match_closest=True, output=False, throw_error=True)
        return True
    except Exception as e:
        print(f"[yellow]Warning in CloseApp: {e}[/yellow]")
        return False
    
#-------------------------------------------
def PlaySong(query: str) -> bool:
    """Play a song - on Spotify if mentioned, else YouTube."""
    query_lower = query.lower()
    
    # If spotify is in the query, open spotify and search there
    if "spotify" in query_lower:
        song = query_lower.replace("spotify", "").strip()
        url = f"https://open.spotify.com/search/{song.replace(' ', '%20')}"
        webopen(url)
        return True
    else:
        # Default: play on YouTube
        try:
            playonyt(query)
            return True
        except Exception as e:
            print(f"[red]Error in PlaySong: {e}[/red]")
            return False    
        
def AmazonSearch(query: str) -> bool:
    """Search for a product on Amazon."""
    try:
        encoded = urllib.parse.quote(query)
        webopen(f"https://www.amazon.in/s?k={encoded}")
        return True
    except Exception as e:
        print(f"[red]Error in AmazonSearch: {e}[/red]")
        return False        

def System(command: str) -> bool:
    """Execute system commands."""
    command = command.lower().strip()
    
    # Volume / media key commands
    key_commands = {
        "mute": "volume mute",
        "unmute": "volume mute",
        "volume up": "volume up",
        "volume down": "volume down"
    }
    
    if command in key_commands:
        try:
            keyboard.press_and_release(key_commands[command])
            return True
        except Exception as e:
            print(f"[red]Error in System command: {e}[/red]")
            return False

    # Screenshot
    elif command in ["screenshot", "take screenshot", "capture screen"]:
        try:
            import datetime
            os.makedirs("Data", exist_ok=True)
            filename = f"Data/screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            subprocess.run(["powershell", "-command",
                f"Add-Type -AssemblyName System.Windows.Forms; "
                f"[System.Windows.Forms.Screen]::PrimaryScreen | Out-Null; "
                f"$bitmap = [System.Drawing.Bitmap]::new([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width, "
                f"[System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height); "
                f"$graphics = [System.Drawing.Graphics]::FromImage($bitmap); "
                f"$graphics.CopyFromScreen(0,0,0,0,$bitmap.Size); "
                f"$bitmap.Save('{filename}')"], capture_output=True)
            print(f"[green]Screenshot saved: {filename}[/green]")
            return True
        except Exception as e:
            print(f"[red]Error taking screenshot: {e}[/red]")
            return False

    # Lock screen
    elif command in ["lock", "lock screen", "lock computer", "lock pc"]:
        try:
            subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
            return True
        except Exception as e:
            print(f"[red]Error locking screen: {e}[/red]")
            return False

    # Shutdown
    elif command in ["shutdown", "shut down", "turn off", "power off"]:
        try:
            subprocess.run(["shutdown", "/s", "/t", "5"])
            print("[yellow]Shutting down in 5 seconds...[/yellow]")
            return True
        except Exception as e:
            print(f"[red]Error in shutdown: {e}[/red]")
            return False

    # Restart
    elif command in ["restart", "reboot"]:
        try:
            subprocess.run(["shutdown", "/r", "/t", "5"])
            print("[yellow]Restarting in 5 seconds...[/yellow]")
            return True
        except Exception as e:
            print(f"[red]Error in restart: {e}[/red]")
            return False

    # Sleep
    elif command in ["sleep", "hibernate", "suspend"]:
        try:
            subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"])
            return True
        except Exception as e:
            print(f"[red]Error in sleep: {e}[/red]")
            return False

    # Brightness up
    elif command in ["brightness up", "increase brightness"]:
        try:
            subprocess.run(["powershell", "-command",
                "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, [math]::Min(100, (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness + 10))"],
                capture_output=True)
            return True
        except Exception as e:
            print(f"[red]Error increasing brightness: {e}[/red]")
            return False

    # Brightness down
    elif command in ["brightness down", "decrease brightness"]:
        try:
            subprocess.run(["powershell", "-command",
                "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, [math]::Max(0, (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness - 10))"],
                capture_output=True)
            return True
        except Exception as e:
            print(f"[red]Error decreasing brightness: {e}[/red]")
            return False

    else:
        print(f"[yellow]Unknown system command: {command}[/yellow]")
        return False


def OpenFolder(folder: str) -> bool:
    """Open common folders in File Explorer."""
    folder = folder.lower().strip()

    folder_paths = {
        "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
        "desktop":   os.path.join(os.path.expanduser("~"), "Desktop"),
        "documents": os.path.join(os.path.expanduser("~"), "Documents"),
        "pictures":  os.path.join(os.path.expanduser("~"), "Pictures"),
        "music":     os.path.join(os.path.expanduser("~"), "Music"),
        "videos":    os.path.join(os.path.expanduser("~"), "Videos"),
    }

    # Check known folders
    for key, path in folder_paths.items():
        if key in folder:
            try:
                subprocess.Popen(["explorer", path])
                return True
            except Exception as e:
                print(f"[red]Error opening folder: {e}[/red]")
                return False

    # Try as a direct path
    if os.path.exists(folder):
        try:
            subprocess.Popen(["explorer", folder])
            return True
        except Exception as e:
            print(f"[red]Error opening folder: {e}[/red]")
            return False

    print(f"[yellow]Folder not found: {folder}[/yellow]")
    return False


def CreateFolder(name: str) -> bool:
    """Create a folder on the Desktop."""
    try:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop", name)
        os.makedirs(desktop, exist_ok=True)
        subprocess.Popen(["explorer", desktop])
        print(f"[green]Folder created: {desktop}[/green]")
        return True
    except Exception as e:
        print(f"[red]Error creating folder: {e}[/red]")
        return False


def ClipboardAction(action: str) -> bool:
    """Read from or clear the clipboard."""
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()

        if "read" in action or "what" in action or "show" in action or "get" in action:
            content = root.clipboard_get()
            root.destroy()
            print(f"[green]Clipboard:[/green] {content}")
            return True

        elif "clear" in action or "empty" in action:
            root.clipboard_clear()
            root.update()
            root.destroy()
            print("[green]Clipboard cleared.[/green]")
            return True

        root.destroy()
        return False
    except Exception as e:
        print(f"[red]Clipboard error: {e}[/red]")
        return False

async def TranslateAndExecute(commands: List[str]) -> AsyncGenerator[Any, None]:
    """Translate and execute commands asynchronously."""
    funcs = []
    
    for command in commands:
        command = command.strip().rstrip('.?!')  # safety net
        if not command:
            continue
                
        try:
            if command.startswith("open "):
                if "open it" in command or "open file" in command:
                    continue
                app_name = command.removeprefix("open").strip()
                funcs.append(OpenAppAsync(app_name))


            #---------------------------------------------
            elif command.startswith("message "):
                # Expected format: "message whatsapp John hello how are you"
                parts = command.removeprefix("message").strip().split(" ", 2)
                if len(parts) >= 3:
                    app, contact, msg_text = parts[0], parts[1], parts[2]
                    if "whatsapp" in app.lower():
                        funcs.append(asyncio.to_thread(SendWhatsAppMessage, contact, msg_text))
                    else:
                        print(f"[yellow]Messaging not supported for: {app}[/yellow]")
                else:
                    print(f"[yellow]Not enough info to send message: {command}[/yellow]")

            elif command.startswith("add to cart "):
                product = command.removeprefix("add to cart").strip()
                funcs.append(asyncio.to_thread(AddToAmazonCart, product))
            
#----------------------------------------------------------------------------------------------------

            elif command.startswith("close "):
                app_name = command.removeprefix("close").strip()
                funcs.append(asyncio.to_thread(CloseApp, app_name))
                
            elif command.startswith("play "):
                query = command.removeprefix("play").strip()
                funcs.append(asyncio.to_thread(PlaySong, query))  # ← was PlayYoutube
                
            elif command.startswith("content "):
                topic = command.removeprefix("content").strip()
                funcs.append(asyncio.to_thread(Content, topic))
                
            elif command.startswith("google search "):
                query = command.removeprefix("google search").strip()
                funcs.append(asyncio.to_thread(GoogleSearch, query))

            elif command.startswith("amazon search "):
                query = command.removeprefix("amazon search").strip()
                funcs.append(asyncio.to_thread(AmazonSearch, query))    
                
            elif command.startswith("system "):
                sys_command = command.removeprefix("system").strip()
                funcs.append(asyncio.to_thread(System, sys_command))

            elif command.startswith("youtube search "):
                query = command.removeprefix("youtube search").strip()
                funcs.append(asyncio.to_thread(YouTubeSearch, query))

            elif command.startswith("open folder "):
                folder = command.removeprefix("open folder").strip()
                funcs.append(asyncio.to_thread(OpenFolder, folder))

            elif command.startswith("create folder "):
                name = command.removeprefix("create folder").strip()
                funcs.append(asyncio.to_thread(CreateFolder, name))

            elif command.startswith("clipboard "):
                action = command.removeprefix("clipboard").strip()
                funcs.append(asyncio.to_thread(ClipboardAction, action))

            else:
                print(f"[yellow]No handler for command: {command}[/yellow]")
                
        except Exception as e:
            print(f"[red]Error processing command {command}: {e}[/red]")
    
    if funcs:
        try:
            results = await asyncio.gather(*funcs, return_exceptions=True)
            for result in results:
                if isinstance(result, Exception):
                    print(f"[red]Command execution error: {result}[/red]")
                else:
                    yield result
        except Exception as e:
            print(f"[red]Error in command execution: {e}[/red]")

async def Automation(commands: List[str]) -> bool:
    """Automate command execution."""
    try:
        async for _ in TranslateAndExecute(commands):
            pass
        return True
    except Exception as e:
        print(f"[red]Error in Automation: {e}[/red]")
        return False