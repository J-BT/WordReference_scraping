import requests
from bs4 import BeautifulSoup


def getTranslation(word_to_search, language_origin, language_destination):
    """
    Search a word's translations with web app 'WordReference'.
    For now you can search :
        English -> French and French -> English
    It returns a dictionnary of dictionnaries as follows:
    
    english_french_dict["word_n1"] = {"eng" : "hello", "fr" : "bonjour"}
    english_french_dict["word_n2"] = {"eng" : "hello", "fr" : "allo"}
    
    ...And so on
    
    
    """
    langFrom = ""
    langTo = ""

    if language_origin == "English":
        langFrom = "en"
    elif language_origin == "French":
        langFrom = "fr"

    if language_destination == "English":
        langTo = "en"
    elif language_destination == "French":
        langTo = "fr"

    if language_origin == language_destination:
        return {"error" : "Please choose 2 different languages..."}

    page = requests.get(f"https://www.wordreference.com/{langFrom}{langTo}/{word_to_search}")
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # displays English inputs
    english_stuffs = soup.find_all("td", class_="FrWrd")
    english_list = list(english_stuffs)

    english_french_dict = {}

    line = 0
    for stuff in english_list:
        stuff = stuff.get_text() # let's remove all tags
        stuff = str(stuff)
        if not "Anglais" in stuff and not "Français" in stuff :
            english_french_dict[f"word_n{line + 1}"] = {"eng" : stuff, "fr" : "" }

            line += 1

    # displays French translations
    french_stuffs = soup.find_all("td", class_="ToWrd")
    french_stuffs = list(french_stuffs)

    line = 0
    for stuff in french_stuffs:
        stuff = stuff.get_text() # let's remove all tags
        stuff = str(stuff)
        if not "Français" in stuff and not "Anglais" in stuff:
            if 0 <= line <len(english_french_dict):
                english_french_dict[f"word_n{line + 1}"]["fr"] = stuff
                line += 1
                        
    return english_french_dict

def getPhonetic(word, language, variant="UK") :
    """
    Search a word's phonetic in 'WordReference'.
    You can use 'English' language and two variants are available : 'US' and 'UK'
    It will return you a string containing the phonetic transcription of the word pronunciation
    """

    langFrom = ""
    langTo = ""

    if language == "English":
        langFrom = "en"
        langTo = "fr"

    page = requests.get(f"https://www.wordreference.com/{langFrom}{langTo}/{word}")
    soup = BeautifulSoup(page.content, 'html.parser')

    pronuncation = soup.find("div", {"id":"pronunciation_widget"}).text

    if variant == "US" and "US" in pronuncation.split('/')[2]:
        return pronuncation.split('/')[3]
    else :
        return pronuncation.split('/')[1]