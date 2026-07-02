import os
import re

DICT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dictionaries'))
MISSING_PATH = os.path.join(DICT_DIR, 'missing_compounds.txt')
CHAR_DICT_PATH = os.path.join(DICT_DIR, 'HanViet_CharDict.txt')

def load_char_dict():
    char_map = {}
    if not os.path.exists(CHAR_DICT_PATH):
        print(f"Error: {CHAR_DICT_PATH} not found.")
        return char_map
    with open(CHAR_DICT_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('=', 1)
            if len(parts) == 2:
                char = parts[0].strip()
                reading = parts[1].strip().lstrip('~') # Remove leading ~ if any
                if char and reading:
                    char_map[char] = reading
    return char_map

def is_number_word(word):
    # Chinese digits and units
    num_chars = set("零一二三四五六七八九十百千万亿拾佰仟萬億两两")
    # Also ignore words that are completely composed of numbers, quantifiers, etc.
    counter_chars = set("个只只只条条块块支支张张面面本本朵朵颗颗间间")
    all_num_set = num_chars.union(counter_chars)
    return all(c in all_num_set for c in word)

def analyze():
    if not os.path.exists(MISSING_PATH):
        print(f"Error: {MISSING_PATH} not found.")
        return

    char_map = load_char_dict()
    print(f"Loaded {len(char_map)} characters from HanViet_CharDict.txt")

    total_words = 0
    total_readings = 0
    max_readings = 0
    max_readings_word = ""
    max_readings_list = []
    
    number_words_count = 0
    cleanable_words = []
    
    with open(MISSING_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            parts = line.split('=', 1)
            if len(parts) != 2:
                continue
            
            total_words += 1
            word = parts[0].strip()
            readings = parts[1].split('/')
            num_readings = len(readings)
            
            total_readings += num_readings
            if num_readings > max_readings:
                max_readings = num_readings
                max_readings_word = word
                max_readings_list = readings
            
            if is_number_word(word):
                number_words_count += 1
            else:
                # Let's see if we can get preferred reading
                pref_parts = []
                for char in word:
                    pref_parts.append(char_map.get(char, char))
                pref_reading = " ".join(pref_parts)
                # Lowercase comparison
                pref_reading_lower = pref_reading.lower()
                readings_lower = [r.lower() for r in readings]
                
                # Check if preferred reading matches one of the readings
                if pref_reading_lower in readings_lower:
                    cleanable_words.append((word, pref_reading, readings))

    print("\n--- ANALYSIS RESULTS ---")
    print(f"Total entries: {total_words}")
    print(f"Average readings per word: {total_readings / total_words:.2f}")
    print(f"Word with most readings: {max_readings_word} ({max_readings} readings)")
    print(f"Example readings of '{max_readings_word}': {max_readings_list[:5]} ...")
    print(f"Number-based entries (to filter out): {number_words_count} ({number_words_count / total_words * 100:.2f}%)")
    print(f"Non-number entries: {total_words - number_words_count}")
    print(f"Entries matching Preferred Char Reading: {len(cleanable_words)} ({len(cleanable_words) / total_words * 100:.2f}%)")
    
    print("\nSample cleaned words:")
    for word, pref, orig in cleanable_words[:15]:
        print(f"  {word} -> {pref} (Original: {orig})")

if __name__ == '__main__':
    analyze()
