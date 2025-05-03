import os
import re
import string
import unicodedata
import numpy as np
from collections import defaultdict, Counter, namedtuple

import diacritization_stripping_data
from preprocessing import clean_text
from generate_subword_freq_class import TokenFrequencyAnalyzer
from diacritization_stripping_class import DiacritizationStripper


def corpus_creation(lan, file, file_desc):

    is_latin = False if lan in ['heb', 'hbo', 'arb'] else True
    clean_file = f'Clean_corpuses/{file_desc}_clean.txt'
    undiac_file = f'Undiac_corpuses/{file_desc}_undiac.txt'
    output_file = f'Output/{file_desc}_freq.txt'

    clean_text(file, clean_file)
    print('finish cleaning')

    text = open(clean_file, encoding="utf8").read()
    stripper = DiacritizationStripper(use_uninorms=True, verbose=True)

    if is_latin:
        stripper_text = stripper.process_text(text)
    else:
        stripper_text = stripper.process_text_without_map(text)


    f = open(undiac_file, "w", encoding="utf8").write(stripper_text)

    stripper.print_statistics()

    analyzer = TokenFrequencyAnalyzer()
    analyzer.analyze_files(undiac_file,  clean_file, output_file, is_latin)
    print('finish ', lan)


if __name__ == "__main__":

    for corp in ['vie_ViLext-train', 'vie_ViLext-dev', 'vie_ViLext-test']:
        file_name = f'Corpuses/{corp}.txt'
        lan = corp.split('_')[0]
        file_desc = corp.split('_')[1]
        corpus_creation(lan, file_name, file_desc)
