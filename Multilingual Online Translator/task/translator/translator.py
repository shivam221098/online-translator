from logic import languages, translate_logic
import sys
import requests
from bs4 import BeautifulSoup


def translate_logic_sys(sentences, translates_from, translates_to):
    from_to = translates_from.lower() + "-" + translates_to.lower() + "/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}

    request = ""
    try:
        request = req.get("https://context.reverso.net/translation/" + from_to + sentences, headers=headers)
    except requests.exceptions.ConnectionError:
        print("Something wrong with your internet connection")
        exit(0)

    file = open(f"{sentences}.txt", "a", encoding="utf-8")  # Opening file with name same as sentence

    print(f"\n{translates_to} Translations:")
    file.writelines(f"{translates_to} Translations:\n")  # Writing contents to file

    soup = BeautifulSoup(request.content, "html.parser")
    translated = soup.find_all(["div"], {"id": "translations-content"})
    translated_words = []
    for translate in translated:
        translated_words.append(translate.get_text().strip())

    try:
        translated_words = translated_words[0].split()
    except IndexError:
        print(f"Sorry, unable to find {sentences}")
        exit(0)

    for i in range(5):
        print(translated_words[i])
        file.writelines(translated_words[i] + "\n")

    translated = soup.find_all(["div"], {"class": "example"})
    src_with_translation = []
    for translate in translated:
        src_trans = translate.get_text().split("\n")
        for sentences in src_trans:
            if len(sentences) > 0:
                src_with_translation.append(sentences.strip())

    print(f"\n{translates_to} Examples:")
    file.writelines(f"\n{translates_to} Examples:\n")

    line_break = 0
    for i in range(10):
        if line_break == 2:
            print()
            file.write("\n")
            line_break = 0
        print(src_with_translation[i])
        file.writelines(src_with_translation[i] + "\n")
        line_break += 1

    file.close()  # Closes the file


arg = sys.argv
req = requests.Session()

"""if len(arg) == 0:
    print("Hello, you're welcome to the translator.")
    print("Translator supports:")
    for key, value in languages.items():
        print(f"{str(key)}. {value}")
    translate_from = input("Type the number of your language:")
    translate_to = input("Type the number of language you want to translate to or 0 to translate to all languages:")
    sentence = input("Type the word you want to translate:")

    if translate_to == "0":
        for key, value in languages.items():
            if key != translate_from:
                translate_logic(sentence, translate_from, key)

    else:
        translate_logic(sentence, translate_from, translate_to)"""

if arg[2].lower() == "all":
    for key, value in languages.items():
        if value.lower() != arg[1]:
            translate_logic_sys(arg[3], arg[1], value)

elif arg[2].title() not in languages.values():
    print(f"Sorry, the program doesn't support {arg[2]}")
    exit(0)

else:
    translate_logic_sys(arg[3], arg[1], arg[2])

