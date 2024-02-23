from hunspell import HunSpell

hobj = HunSpell('/usr/share/hunspell/en_US.dic', '/usr/share/hunspell/en_US.aff')

def correct_word(w, params):
    if not hobj.spell(w):
        suggestions = hobj.suggest(w)
        if len(suggestions) > 0:
            return suggestions[0]
    return w