import string
import re

def clean_text(input_file, output_file):
    text = open(input_file, encoding="utf8").read()
    text = text.replace('.', '\n')
    text = re.sub(r'[؛؟،]', ' ', text)
    remove_dict = str.maketrans('', '', string.punctuation + string.digits)
    cleaned_corpus = text.translate(remove_dict)
    lines = cleaned_corpus.split('\n')
    filtered_lines = []

    for line in lines:
        filtered_line = ' '.join(line.split())
        filtered_lines.append(filtered_line)

    final_corpus = '\n'.join(filtered_lines)
    f = open(output_file, "w", encoding="utf8").write(final_corpus)