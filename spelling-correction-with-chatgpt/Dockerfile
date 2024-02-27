#docker build -t registry.webis.de/code-research/tira/tira-user-qspell/parse-chatgpt-responses .
FROM python

RUN pip3 install pandas

ADD extract_predictions.py /extract_predictions.py

ENTRYPOINT [ "/extract_predictions.py", "--input", "$inputRun", "--output", "$outputDir" ]
