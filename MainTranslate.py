import requests

# LibreTranslate API endpoint (use a public instance or our own)
LIBRETRANSLATE_URL = "http://localhost:5000/translate"

def translate_text(text, target_language):
    # Prepare the request payload
    payload = {
        "q": text,
        "source": "auto",
        "target": target_language,
        "format": "text"
    }

    # Add headers (optional, but some instances may require it)
    headers = {
        "Content-Type": "application/json"
    }

    # Send the POST request to LibreTranslate
    response = requests.post(LIBRETRANSLATE_URL, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        translated_text = response.json().get("translatedText")
        detected_language = response.json().get("detectedLanguage", {}).get("language")
        return translated_text, detected_language
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None, None

def main():
    # Get user input
    text_to_translate = input("Enter the sentence you want to translate: ")
    target_language = input("Enter the language code you want to translate to (e.g., 'es' for Spanish, 'fr' for French): ")

    # Translate the text
    translated_text, detected_language = translate_text(text_to_translate, target_language)

    # Display the results
    if translated_text:
        print(f"\nOriginal Text: {text_to_translate}")
        print(f"Detected Language: {detected_language}")
        print(f"Translated Text: {translated_text}")
    else:
        print("Translation failed. Please try again.")

if __name__ == "__main__":
    main()

#The following are commands to run on terminal to activate the docker that was installed onto pc

#Use this to run a docker with all languages (WARNING IT WILL TAKE A LONG TIME)
#docker run -it -p 5000:5000 libretranslate/libretranslate

#This will limit the amount of languages that are downloaded
#docker run -it -p 5000:5000 libretranslate/libretranslate --load-only en,es,fr