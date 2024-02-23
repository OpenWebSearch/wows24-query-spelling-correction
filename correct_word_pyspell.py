from spellchecker import SpellChecker

spell = SpellChecker()

# from https://github.com/ielab/CharacterBERT-DR/blob/main/data/py_spellchecker.py

def correct_word(word, params):
    misspelled = spell.unknown([word])
    if len(misspelled) != 0:
        ret = spell.correction(word)
        return ret if ret else ''
    return word if word else ''