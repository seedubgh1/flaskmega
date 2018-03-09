from googletrans import Translator

def translate(text, source_language, dest_language):
    translator = Translator()

    translation =  translator.translate(text=text
                               ,src=source_language
                               ,dest=dest_language).text

    return translation if translation else '<could not translate>'
