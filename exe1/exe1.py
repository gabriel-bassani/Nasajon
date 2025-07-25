import xml.etree.ElementTree as ET
from deep_translator import GoogleTranslator 

INPUT_FILE = "localization.xml"
OUTPUT_FILE = "localization_ptbr.xml"
ORIGINAL_LANG = "en"
DESTINY_LENG = "pt"

def translateText(text, origin=ORIGINAL_LANG, destiny=DESTINY_LENG):
    try:
        return GoogleTranslator(source=origin, target=destiny).translate(text)
    except Exception as e:
        print(f"Erro ao traduzir '{text}': {e}")
        return text 

ET.register_namespace('', "http://nasajon.com/schemas/localization.xsd")
tree = ET.parse(INPUT_FILE)
root = tree.getroot()
root.set("culture", "pt-BR")

for stringEle in root.iter("{http://nasajon.com/schemas/localization.xsd}string"):
    originalText = stringEle.text
    if originalText:
        translatedText = translateText(originalText)
        print(f"'{originalText}' → '{translatedText}'")
        stringEle.text = translatedText

tree.write(OUTPUT_FILE, encoding="utf-8", xml_declaration=True)
print(f"\nArquivo traduzido: {OUTPUT_FILE}")
