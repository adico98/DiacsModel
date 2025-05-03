import argparse
from collections import Counter
from transformers import AutoTokenizer
from subword_freq_utils import get_aligned_tokens, get_aligned_heb_tokens

class TokenFrequencyAnalyzer:
    def __init__(self, model='bert-base-multilingual-uncased'):
        # Initialize the tokenizer with a specified model
        self.tokenizer = AutoTokenizer.from_pretrained(model, use_fast=True)

    def analyze_latin_files(self, cnt, input_file, target_file):
        # Read and process each line from the input and target files
        with open(input_file, 'r', encoding="utf8") as reader_input, open(target_file, 'r',
                                                                          encoding="utf8") as reader_target:
            for input_line, target_line in zip(reader_input, reader_target):
                aligned_tokens = get_aligned_tokens(input_line.strip(), target_line.strip(), self.tokenizer)
                tokens_dia = [x[1] for x in aligned_tokens]
                cnt.update(tokens_dia)

        return cnt

    def analyze_non_latin_files(self, cnt, input_file, target_file):
        # Read and process each line from the input and target files
        with open(input_file, 'r', encoding="utf8") as reader_input, open(target_file, 'r',
                                                                          encoding="utf8") as reader_target:
            for input_line, target_line in zip(reader_input, reader_target):
                aligned_tokens = get_aligned_heb_tokens(input_line.strip(), target_line.strip(), self.tokenizer)
                tokens_dia = [x[1] for x in aligned_tokens]
                cnt.update(tokens_dia)

        return cnt

    def analyze_files(self, input_file, target_file, output_file, is_latin):
        # Counter to hold token frequencies
        cnt = Counter()

        if is_latin:
            cnt = self.analyze_latin_files(cnt, input_file, target_file)
        else:
            cnt = self.analyze_non_latin_files(cnt, input_file, target_file)

        # Write the token frequencies to the output file
        with open(output_file, 'w', encoding="utf8") as out_writer:
            for token, token_count in cnt.most_common():
                out_writer.write(f"{token}\t{token_count}\n")


