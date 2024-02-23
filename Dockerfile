#docker build -t webis/query-spelling-correction:0.0.1 .
FROM webis/query-spelling-correction:0.0.1-dev

ADD wikipedia_common_misspellings.csv /code/
ADD lookup_dict_rushton.csv /code/
ADD correct_query.py correct_word_rushton.py correct_word_hunspell.py correct_word_pyspell.py /code/

WORKDIR /code

ENTRYPOINT [ "python3", "/code/correct_query.py" ]
