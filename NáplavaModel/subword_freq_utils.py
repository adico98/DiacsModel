import unicodedata

def get_aligned_tokens(input_line, target_line, tokenizer):
    unk_token = tokenizer.unk_token

    if not tokenizer.is_fast:
        raise ValueError("Do use fast tokenizer!")

    else:
        tokens_nodia_alignment = get_token_source_mapping(input_line, tokenizer)
        tokens_nodia = []
        tokens_dia = []
        cur_diac_tok_start = 0

        for cur_tok, cur_tok_start, cur_tok_end in tokens_nodia_alignment:
            tokens_nodia.append(cur_tok)
            tokens_dia.append(target_line[cur_tok_start:cur_tok_end])

        aligned_tokens = []
        for token_nodia, token_dia in zip(tokens_nodia, tokens_dia):
            if token_nodia.startswith('##') and not token_dia.startswith('##'):
                token_dia = '##' + token_dia

            if token_nodia.startswith('▁') and not token_dia.startswith('▁'):
                token_dia = '▁' + token_dia

            if len(token_nodia) == len(token_dia):
                aligned_tokens.append([token_nodia, token_dia])

        return aligned_tokens


def get_aligned_heb_tokens(input_line, target_line, tokenizer):
    unk_token = tokenizer.unk_token

    if not tokenizer.is_fast:
        raise ValueError("Do use fast tokenizer!")

    else:
        tokens_nodia_alignment = get_token_source_mapping(input_line, tokenizer)
        tokens_nodia = []
        tokens_dia = []
        cur_diac_tok_start = 0
        prev_end = 0

        for cur_tok, cur_tok_start, cur_tok_end in tokens_nodia_alignment:
            tokens_nodia.append(cur_tok)
            cur_diac_tok_start +=cur_tok_start - prev_end
            diac_tok_len = heb_arb_diacs(target_line, cur_tok_start, cur_tok_end, cur_diac_tok_start)
            tokens_dia.append(target_line[cur_diac_tok_start:cur_diac_tok_start + diac_tok_len])
            cur_diac_tok_start += diac_tok_len
            prev_end = cur_tok_end

        aligned_tokens = []
        for token_nodia, token_dia in zip(tokens_nodia, tokens_dia):
            if token_nodia.startswith('##') and not token_dia.startswith('##'):
                token_dia = '##' + token_dia

            if token_nodia.startswith('▁') and not token_dia.startswith('▁'):
                token_dia = '▁' + token_dia

            aligned_tokens.append([token_nodia, token_dia])

        return aligned_tokens


def heb_arb_diacs(text, start, end, diac_start):
    letters_amount = end-start
    letters_count = 0
    token_len = 0

    for char in text[diac_start:]:
        # Check if the character is a combining mark
        if unicodedata.combining(char) == 0:
            # If not a combining mark and base_char has content, append it to results
            if letters_count == letters_amount:
                return token_len
            letters_count +=1
        token_len +=1

    return token_len

def get_token_source_mapping(input_line, tokenizer):
    unk_token = tokenizer.unk_token

    if not tokenizer.is_fast:
        raise ValueError('Not supported, must use Fast tokenizer!')
    else:
        input_line_encoded = tokenizer(input_line)
        if len(input_line_encoded['input_ids']) > 512:
            print('too long! ', len(input_line_encoded['input_ids']))
            return []

        input_line_tokens = tokenizer.convert_ids_to_tokens(input_line_encoded['input_ids'])
        input_line_tokens_special_out = []
        for input_line_token in input_line_tokens:
            # skip all special tokens (e.g. [CLS], [PAD]) - these are added later, but not unknown token
            if input_line_token in tokenizer.all_special_tokens_extended and input_line_token != unk_token:
                continue

            input_line_tokens_special_out.append(input_line_token)
        input_line_tokens = input_line_tokens_special_out

        input_line_char_to_token_indices = [input_line_encoded.char_to_token(i) for i in range(len(input_line))]
        aligned_tokens = [[x, None, None] for x in input_line_tokens]
        for i in range(len(input_line)):
            cur_char_word_ind = input_line_char_to_token_indices[i]

            if cur_char_word_ind is None:
                continue

            cur_char_word_ind = cur_char_word_ind - 1  # char_to_token indexes from 1
            if aligned_tokens[cur_char_word_ind][1] is None:
                aligned_tokens[cur_char_word_ind][1] = i

            aligned_tokens[cur_char_word_ind][2] = i + 1

        for i in range(len(aligned_tokens)):
            if i > 0 and aligned_tokens[i][1] is None:
                aligned_tokens[i][1] = aligned_tokens[i - 1][1]
                aligned_tokens[i][2] = aligned_tokens[i - 1][2]

        if len(aligned_tokens) != len(input_line_tokens):
            print(input_line)
            print(aligned_tokens)
            print(input_line_tokens)
            raise ValueError()
    return aligned_tokens
