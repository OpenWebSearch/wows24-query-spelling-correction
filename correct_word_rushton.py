import pandas as pd
import os

lookup_dict = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/lookup_dict_rushton.csv', na_filter=False, sep='\t', names=['word', 'correction', 'cosine']).set_index('word')

def correct_word(w, params):
    if w in lookup_dict.index:
        if lookup_dict['cosine'][w] < params['max_cosine']:
            return lookup_dict['correction'][w]
    return w