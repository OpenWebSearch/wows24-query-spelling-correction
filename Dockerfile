#docker build -t webis/query-spelling-correction:0.0.1 .
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update \
	&& apt-get upgrade -y \
	&& apt-get install -y python3 python3-pip python-is-python3 openjdk-11-jdk wget \
	build-essential hunspell-en-us libhunspell-dev python3-dev \
	&& pip3 install jupyter ir_datasets tira>=0.0.89 \
	hunspell pyspellchecker \
	&& rm -Rf /var/cache/apt \
	&& rm -Rf /root/.cache/pip

ADD wikipedia_common_misspellings.csv /code/
ADD lookup_dict_rushton.csv /code/
ADD correct_query.py correct_word_rushton.py correct_word_hunspell.py correct_word_pyspell.py /code/

WORKDIR /code

ENTRYPOINT [ "python3", "/code/correct_query.py" ]
