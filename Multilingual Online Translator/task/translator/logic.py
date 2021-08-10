import requests
from bs4 import BeautifulSoup


languages = {"1": "Arabic",
             "2": "German",
             "3": "English",
             "4": "Spanish",
             "5": "French",
             "6": "Hebrew",
             "7": "Japanese",
             "8": "Dutch",
             "9": "Polish",
             "10": "Portuguese",
             "11": "Romanian",
             "12": "Russian",
             "13": "Turkish"}


req = requests.Session()


def translate_logic(sentence, translate_from, translate_to):
    from_to = languages[translate_from].lower() + "-" + languages[translate_to].lower() + "/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}
    request = req.get("https://context.reverso.net/translation/" + from_to + sentence, headers=headers)

    file = open(f"{sentence}.txt", "a", encoding="utf-8")  # Opening file with name same as sentence

    print(f"\n{languages[translate_to]} Translations:")
    file.writelines(f"{languages[translate_to]} Translations:\n")  # Writing contents to file

    soup = BeautifulSoup(request.content, "html.parser")
    translated = soup.find_all(["div"], {"id": "translations-content"})
    translated_words = []
    for translate in translated:
        translated_words.append(translate.get_text().strip())

    translated_words = translated_words[0].split()
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

    print(f"\n{languages[translate_to]} Examples:")
    file.writelines(f"\n{languages[translate_to]} Examples:\n")

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
