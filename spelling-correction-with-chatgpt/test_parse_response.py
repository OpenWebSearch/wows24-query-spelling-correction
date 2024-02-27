from extract_predictions import parse_response

def test_01():
    chatgpt_output = 'Why do wisdom varies from person to person? \n\nCorrected: Why does wisdom vary from person to person?'
    expected = 'Why does wisdom vary from person to person?'
    
    assert expected == parse_response(chatgpt_output)

def test_02():
    chatgpt_output = 'Why does wisdom vary from person to person?'
    expected = 'Why does wisdom vary from person to person?'
    
    assert expected == parse_response(chatgpt_output)

def test_03():
    chatgpt_output = 'Why do people feed poison (sugar) to their kids on Easter, and why are there no chocolate Jesuses?  \n(Original search query corrected for spelling)'
    expected = 'Why do people feed poison (sugar) to their kids on Easter, and why are there no chocolate Jesuses?'
    
    assert expected == parse_response(chatgpt_output)

def test_04():
    chatgpt_output = '"\"space Renault\" -> \"Space Renault\"'
    expected = '\"Space Renault\"'
    
    assert expected == parse_response(chatgpt_output)

def test_05():
    chatgpt_output = '"\"space Renault\" => \"Space Renault\"'
    expected = '\"Space Renault\"'
    
    assert expected == parse_response(chatgpt_output)
