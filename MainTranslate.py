import requests
from datetime import datetime

# LibreTranslate API endpoint
LIBRETRANSLATE_URL = "http://localhost:5000/translate"

# Supported languages with their codes
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'zh': 'Chinese',
    'ja': 'Japanese',
    'ar': 'Arabic'
}

def translate_text(text, target_language):
    if target_language not in SUPPORTED_LANGUAGES:
        return None, None
    
    payload = {
        "q": text,
        "source": "auto",
        "target": target_language,
        "format": "text"
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(LIBRETRANSLATE_URL, json=payload, headers=headers, timeout=5)
        
        if response.status_code == 200:
            translated_text = response.json().get("translatedText")
            detected_language = response.json().get("detectedLanguage", {}).get("language")
            return translated_text, detected_language
        else:
            print(f"Translation API error: {response.status_code} - {response.text}")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Translation request failed: {str(e)}")
        return None, None

def get_supported_languages():
    return SUPPORTED_LANGUAGES

if __name__ == "__main__":
    # Demo mode
    print("Supported Languages:")
    for code, name in SUPPORTED_LANGUAGES.items():
        print(f"{code}: {name}")
    
    text_to_translate = input("\nEnter text to translate: ")
    target_language = input("Enter target language code: ")
    
    translated_text, detected_language = translate_text(text_to_translate, target_language)
    
    if translated_text:
        print(f"\nOriginal ({detected_language}): {text_to_translate}")
        print(f"Translated ({target_language}): {translated_text}")
    else:
        print("Translation failed.")

#The following are commands to run on terminal to activate the docker that was installed onto pc

#Use this to run a docker with all languages (WARNING IT WILL TAKE A LONG TIME)
#docker run -it -p 5000:5000 libretranslate/libretranslate

#Create a virutal environment for the dependencies then activate it
#python -m venv venv
#.\.venv\Scripts\activate

#Configure VS Code to Use the Virtual Environment

'''
Press Ctrl+Shift+P (Command Palette).

Search for "Python: Select Interpreter".

Choose the Python executable from .venv:

Typically looks like:
./.venv/Scripts/python.exe (Windows)

'''


#First terminal
#This will limit the amount of languages that are downloaded
#docker run -it -p 5000:5000 libretranslate/libretranslate --load-only en,es,fr,de,it,pt,ru,zh,ja,ar

#Second terminal
#python server.py

#third terminal
#python client.py