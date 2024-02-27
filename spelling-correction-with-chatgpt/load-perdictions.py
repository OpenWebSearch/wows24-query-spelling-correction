#!/usr/bin/python3
import json
import pandas as pd
import argparse
from tira.third_party_integrations import ir_datasets
import os
from tqdm import tqdm

prompts = {
    '1': 'You are a spelling corrector for search queries. You respond always exactly with the corrected search query. Please correct all spelling mistakes in the query:\n<QUERY>'
}

TIREX_DATASETS = [
    'antique-test-20230107-training', 'argsme-touche-2021-task-1-20230209-training', 'argsme-touche-2020-task-1-20230209-training',
    'clueweb09-en-trec-web-2009-20230107-training', 'clueweb09-en-trec-web-2010-20230107-training', 'clueweb09-en-trec-web-2011-20230107-training',
    'clueweb09-en-trec-web-2012-20230107-training', 'clueweb12-touche-2020-task-2-20230209-training', 'clueweb12-touche-2021-task-2-20230209-training',
    'clueweb12-trec-misinfo-2019-20240214-training', 'clueweb12-trec-web-2013-20230107-training', 'clueweb12-trec-web-2014-20230107-training',
    'cord19-fulltext-trec-covid-20230107-training', 'cranfield-20230107-training', 'disks45-nocr-trec-robust-2004-20230209-training',
    'disks45-nocr-trec7-20230209-training', 'disks45-nocr-trec8-20230209-training', 'gov-trec-web-2002-20230209-training',
    'gov-trec-web-2003-20230209-training', 'gov-trec-web-2004-20230209-training', 'gov2-trec-tb-2004-20230209-training',
    'gov2-trec-tb-2005-20230209-training', 'gov2-trec-tb-2006-20230209-training', 'longeval-heldout-20230513-training',
    'longeval-long-september-20230513-training', 'longeval-short-july-20230513-training', 'longeval-train-20230513-training',
    'medline-2004-trec-genomics-2004-20230107-training', 'medline-2004-trec-genomics-2005-20230107-training', 'medline-2017-trec-pm-2017-20230211-training',
    'medline-2017-trec-pm-2018-20230211-training', 'msmarco-passage-trec-dl-2019-judged-20230107-training', 'msmarco-passage-trec-dl-2020-judged-20230107-training',
    'nfcorpus-test-20230107-training', 'trec-tip-of-the-tongue-dev-20230607-training', 'vaswani-20230107-training',
    'wapo-v2-trec-core-2018-20230107-training'
]

def process_query(query, prompt):
    import openai
    print(f'Process Query: {query}')

    request = prompts[prompt].replace('<QUERY>', query)
    ret = {'request': request, 'prompt': prompt}
    ret['gpt-3.5-turbo-response'] = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": request}
        ]
    )

    print(f'Response: {ret}')
    
    return ret

def main(prompt, dataset):
    output = f'{dataset}/queries.jsonl'
    covered_queries = set()

    if os.path.exists(output):
        covered_queries = pd.read_json(output, lines=True)['query_id'].astype(str).unique()

    if not os.path.exists(dataset):
        os.mkdir(dataset)

    dataset = ir_datasets.load(f'ir-benchmarks/{dataset}')
    with open(output, 'a+') as output:
        for query in tqdm(dataset.queries_iter()):
            if str(query.query_id) not in covered_queries:
                output.write(json.dumps({'query_id': str(query.query_id), 'response': process_query(query.default_text(), prompt)}) + '\n')
                output.flush()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='SpellingCorrectionWithChatGPT')
    parser.add_argument('--prompt', required=True)
    parser.add_argument('--dataset', required=True, choices=TIREX_DATASETS)

    args = parser.parse_args()

    main(args.prompt, args.dataset)

