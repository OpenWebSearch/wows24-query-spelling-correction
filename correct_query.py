from tira.third_party_integrations import ir_datasets, get_output_directory
from pathlib import Path
import pandas as pd
from tqdm import tqdm

def process_query(query, params):
    return {'qid': query.query_id, 'query': ' '.join([correct_word(w, params) for w in query.default_text().split(' ')])}


def process_queries(queries_iter, params):
    return pd.DataFrame([process_query(i, params) for i in queries_iter])


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description='correct_query')
    parser.add_argument('--method', type=str, default='rushton', help='Method to use for correction')
    parser.add_argument('--max_cosine', type=float, default=1.0, help='Maximum cosine similarity to consider a word as correct')
    parser.add_argument('--dataset', type=str, default='workshop-on-open-web-search/query-processing-20231027-training', help='The tira/ir_dataset id to process')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    # In the TIRA sandbox, this is the injected ir_dataset, injected via the environment variable TIRA_INPUT_DIRECTORY
    dataset = ir_datasets.load(args.dataset)

    # The expected output directory, injected via the environment variable TIRA_OUTPUT_DIRECTORY
    output_dir = get_output_directory('.')
    
    output_file = Path(output_dir) / 'queries.jsonl'


    if args.method == 'rushton':
        from correct_word_rushton import correct_word
    elif args.method == 'pyspell':
        from correct_word_pyspell import correct_word
    elif args.method == 'hunspell':
        from correct_word_hunspell import correct_word
    else:
        raise ValueError(f'Unknown method {args.method}')
        
    params = {
        'max_cosine': args.max_cosine
    }
    
    # process the queries, store results at expected location.
    processed_queries = process_queries(tqdm(list(dataset.queries_iter())), params)
    processed_queries.to_json(output_file, lines=True, orient='records')
