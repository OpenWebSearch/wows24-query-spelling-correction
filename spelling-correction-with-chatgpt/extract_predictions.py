#!/usr/bin/env python3
import pandas as pd

def parse_response(i):
    if 'Corrected:' in i:
        return parse_response(i.split('Corrected:')[-1])
    if '\n(' in i:
        return parse_response(i.split('\n(')[0])
    if '->' in i:
        return parse_response(i.split('->')[-1])
    if '=>' in i:
        return parse_response(i.split('=>')[-1])
    return i.strip()
    

def main(input_directory, output_directory):
    queries = pd.read_json(input_directory + '/queries.jsonl', lines=True)
    ret = []

    for _, i in queries.iterrows():
        ret += [{'query_id': str(i['query_id']), 'query': parse_response(i['response']['gpt-3.5-turbo-response']['choices'][0]['message']['content'])}]

    pd.DataFrame(ret).to_json(output_directory + '/queries.jsonl', lines=True, orient='records')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog='parse-spelling-correction-response')
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)

    args = parser.parse_args()

    main(args.input, args.output)

