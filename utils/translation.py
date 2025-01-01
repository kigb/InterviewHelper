import requests

def translate_cn_to_en(text, api_key):
    """
    Translate Chinese text to English using DeepL API.
    
    :param text: The Chinese text to translate
    :param api_key: The API key for DeepL API
    :return: Translated English text
    """
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": api_key,
        "text": text,
        "target_lang": "EN"
    }
    
    response = requests.post(url, data=params)
    
    if response.status_code == 200:
        result = response.json()
        return result['translations'][0]['text']
    else:
        return f"Error: {response.status_code}, {response.text}"
