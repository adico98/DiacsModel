import unicodedata

class DiacritizationStripper:
    def __init__(self, use_uninorms=False, verbose=False):
        import diacritization_stripping_data
        self.verbose = verbose
        if use_uninorms:
            self.maps = [diacritization_stripping_data.strip_diacritization_uninorms]
        else:
            self.maps = [diacritization_stripping_data.strip_diacritization_uninames]
        self.stripped_map = {}
        self.total = 0
        self.stripped = 0

    def process_text(self, text):
        output = ""
        for line in text.splitlines():
            line = unicodedata.normalize('NFC', line)
            for c in line:
                for m in self.maps:
                    if c in m:
                        self.stripped += 1
                        self.stripped_map[c] = self.stripped_map.get(c, 0) + 1
                        output += m[c]
                        break
                else:
                    output += c
                if not c.isspace():
                    self.total += 1
            output += '\n'
        return output

    def process_text_without_map(self, text):
        output = ""
        # using nfc, will make the diac come AFTER the letter they belong to. so we can just take the first letter in the cell
        for line in text.splitlines():
            for word in line.split():
                split_word = self.split_diac(word)
                for c in split_word:
                    if len(c) > 1:
                        self.stripped += 1
                        # check how to get undiac char ?
                        self.stripped_map[c] = self.stripped_map.get(c, 0) + 1
                        output += c[0]
                    else:
                        output += c
                    self.total +=1
                output += ' '
            output += '\n'
        return output

    def split_diac(self, word):
        result = []
        base_char = ''  # This will hold the base character and any combining marks
        word = unicodedata.normalize('NFD', word)

        for char in word:
            # Check if the character is a combining mark
            if unicodedata.combining(char) == 0:
                # If not a combining mark and base_char has content, append it to results
                if base_char:
                    result.append(base_char)
                base_char = char  # Start new base character
            else:
                # If it is a combining mark, add it to the current base character
                base_char += char

        # Append the last accumulated character
        if base_char:
            result.append(base_char)

        return result
    def print_statistics(self):
        if self.verbose:
            histogram = sorted(self.stripped_map.items(), key=lambda kv: kv[1], reverse=True)[:10]
            histogram = " ".join("{}:{:.2f}%".format(k, 100 * v / self.stripped) for k, v in histogram)
            print(f"Total: {self.total}, Stripped: {100 * self.stripped / self.total:.2f}%, Histogram: {histogram}")


