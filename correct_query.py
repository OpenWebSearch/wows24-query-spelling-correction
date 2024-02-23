from tira.third_party_integrations import ir_datasets, get_output_directory
from pathlib import Path
import pandas as pd

def process_query(query, params):
    return {'qid': query.query_id, 'query': ' '.join([correct_word(w, params) for w in query.default_text().split(' ')])}


def process_queries(queries_iter, params):
    return pd.DataFrame([process_query(i, params) for i in queries_iter])


if __name__ == '__main__':
    # In the TIRA sandbox, this is the injected ir_dataset, injected via the environment variable TIRA_INPUT_DIRECTORY
    dataset = ir_datasets.load('workshop-on-open-web-search/query-processing-20231027-training')

    # The expected output directory, injected via the environment variable TIRA_OUTPUT_DIRECTORY
    output_dir = get_output_directory('.')
    
    # Query processors persist their results in a file queries.jsonl in the output directory.
    output_file = Path(output_dir) / 'queries.jsonl'
    
    # You can pass as many additional arguments to your program, e.g., via argparse, to modify the behaviour

    method = 'rushton'

    if method == 'rushton':
        from correct_word_rushton import correct_word
    elif method == 'pyspell':
        from correct_word_pyspell import correct_word
    elif method == 'hunspell':
        from correct_word_hunspell import correct_word
        
    params = {
        'max_cosine': 1.0
    }
    
    #TODO: allow to overwrite method and max_cosine using command line args
    
    # process the queries, store results at expected location.
    processed_queries = process_queries(dataset.queries_iter(), params)
    processed_queries.to_json(output_file, lines=True, orient='records')