
import unicodedata

def split_hebrew_with_diacritics(text):
    result = []
    base_char = ''  # This will hold the base character and any combining marks

    for char in text:
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

# Example usage
hebrew_text = 'רוֹשֶׁם'
chars_with_diacritics = split_hebrew_with_diacritics(hebrew_text)
print(chars_with_diacritics)
