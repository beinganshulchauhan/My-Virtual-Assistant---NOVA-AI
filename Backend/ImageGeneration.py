# from PIL import Image
# import requests
# import os
# from time import sleep

# # Function to open and display images based on a given prompt
# def open_images(prompt):
#     folder_path = r"Data"
#     prompt_clean = prompt.replace(" ", "_")
#     Files = [f"{prompt_clean}{i}.jpg" for i in range(1, 2)]

#     for jpg_file in Files:
#         image_path = os.path.join(folder_path, jpg_file)
#         try:
#             img = Image.open(image_path)
#             print(f"Opening image: {image_path}")
#             img.show()
#             sleep(1)
#         except IOError:
#             print(f"Unable to open {image_path}")

# # Query Pollinations AI — no API key needed
# def query(prompt, seed):
#     for attempt in range(3):
#         try:
#             url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}?seed={seed}&width=1024&height=1024&nologo=true"
#             print(f"Requesting (attempt {attempt + 1}): {url}")
#             response = requests.get(url, timeout=120)

#             if response.status_code == 200:
#                 print("Image received!")
#                 return response.content
#             else:
#                 print(f"Error {response.status_code}: {response.text}")

#         except requests.exceptions.Timeout:
#             print(f"Timed out on attempt {attempt + 1}, retrying...")
#             sleep(5)

#         except KeyboardInterrupt:  # ← catch the interrupt
#             print("Request interrupted, retrying...")
#             sleep(5)

#         except Exception as e:
#             print(f"Error on attempt {attempt + 1}:", repr(e))
#             sleep(5)

#     print("All attempts failed, skipping.")
#     return None

# # Generate 4 images with different seeds
# def generate_images(prompt: str):
#     os.makedirs("Data", exist_ok=True)  # Create Data folder if it doesn't exist
#     prompt_clean = prompt.replace(" ", "_")

#     for i in range(1, 2):
#         seed = i * 1000  # Different seed for each image
#         print(f"Generating image {i} of 1...")
#         image_bytes = query(prompt, seed)

#         if image_bytes:
#             path = os.path.join("Data", f"{prompt_clean}{i}.jpg")
#             with open(path, "wb") as f:
#                 f.write(image_bytes)
#             print(f"Saved image {i}: {path}")
#         else:
#             print(f"Failed to generate image {i}")

# # Wrapper — generate then open
# def GenerateImages(prompt: str):
#     generate_images(prompt)
#     open_images(prompt)

# # Main loop — monitors the data file
# while True:
#     try:
#         with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
#             Data: str = f.read()

#         Prompt, Status = Data.split(",")

#         if Status.strip() == "True":
#             # Reset file before generating
#             with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
#                 f.write("False,False")

#             print("Generating Images.....")
#             GenerateImages(prompt=Prompt)

#             # Reset file after generating
#             with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
#                 f.write("False,False")

#             break

#         else:
#             sleep(1)

#     except Exception as e:
#         print(f"Error: {e}")
#         sleep(1)


from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep

# Function to open and display images
def open_images(prompt):
    folder_path = r"Data"
    prompt_clean = prompt.replace(" ", "_")
    Files = [f"{prompt_clean}{i}.jpg" for i in range(1, 2)]  # 1 image

    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)
        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to open {image_path}")

# API details
API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
headers = {
    "Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"
}

def query(prompt, seed):
    for attempt in range(3):  # Retry up to 3 times
        try:
            print(f"Attempt {attempt + 1} — sending request...")
            response = requests.post(
                API_URL,
                headers=headers,
                json={
                    "inputs": prompt,
                    "parameters": {"seed": seed}
                },
                timeout=(15, 300)
            )

            if response.status_code == 200:
                print("Image received!")
                return response.content

            elif response.status_code == 503:
                wait = response.json().get("estimated_time", 30)
                print(f"Model loading, waiting {wait:.0f} seconds...")
                sleep(wait)

            elif response.status_code == 401:
                print("Invalid API key — check your HuggingFace token in .env")
                return None

            else:
                print(f"API Error {response.status_code}:", response.text)
                sleep(5)

        except requests.exceptions.Timeout:
            print(f"Timed out on attempt {attempt + 1}, retrying...")
            sleep(5)

        except KeyboardInterrupt:
            print("Interrupted, retrying...")
            sleep(5)

        except Exception as e:
            print(f"Error on attempt {attempt + 1}:", repr(e))
            sleep(5)

    print("All attempts failed, skipping.")
    return None

def generate_images(prompt: str):
    os.makedirs("Data", exist_ok=True)
    prompt_clean = prompt.replace(" ", "_")

    seed = 1000
    print(f"Generating image...")
    image_bytes = query(prompt, seed)

    if image_bytes:
        path = os.path.join("Data", f"{prompt_clean}1.jpg")
        with open(path, "wb") as f:
            f.write(image_bytes)
        print(f"Saved image: {path}")
    else:
        print("Failed to generate image")

def GenerateImages(prompt: str):
    generate_images(prompt)
    open_images(prompt)

# Main loop
while True:
    try:
        with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
            Data: str = f.read()

        Prompt, Status = Data.split(",")

        if Status.strip() == "True":
            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False,False")

            print("Generating Images.....")
            GenerateImages(prompt=Prompt)

            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False,False")
            break

        else:
            sleep(1)

    except Exception as e:
        print(f"Error: {e}")
        sleep(1)