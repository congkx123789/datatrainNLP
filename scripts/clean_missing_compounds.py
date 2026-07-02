import os
import re

DICT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dictionaries'))
MISSING_PATH = os.path.join(DICT_DIR, 'missing_compounds.txt')
CHAR_DICT_PATH = os.path.join(DICT_DIR, 'HanViet_CharDict.txt')
OUTPUT_PATH = os.path.join(DICT_DIR, 'missing_compounds_cleaned.txt')

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
    # Chinese digits, units and common counters
    num_chars = set("零一二三四五六七八九十百千万亿拾佰仟萬億两两")
    counter_chars = set("个只只只条条块块支支张张面面本本朵朵颗颗间间")
    all_num_set = num_chars.union(counter_chars)
    return all(c in all_num_set for c in word)

def clean_dictionary():
    if not os.path.exists(MISSING_PATH):
        print(f"Error: {MISSING_PATH} not found.")
        return

    char_map = load_char_dict()
    print(f"Loaded {len(char_map)} characters from HanViet_CharDict.txt")

    total_words = 0
    written_count = 0
    filtered_numbers = 0
    fallback_count = 0

    print(f"Cleaning {MISSING_PATH} -> {OUTPUT_PATH}...")

    with open(MISSING_PATH, 'r', encoding='utf-8') as fin, open(OUTPUT_PATH, 'w', encoding='utf-8') as fout:
        # Write header
        fout.write("# Cleaned list of Chinese compounds missing in Aligned_HanViet.txt\n")
        fout.write("# Aligned to a single preferred reading using HanViet_CharDict.txt\n")
        fout.write("# Format: Word=HV_Reading\n\n")

        for line in fin:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            parts = line.split('=', 1)
            if len(parts) != 2:
                continue

            total_words += 1
            word = parts[0].strip()
            readings = [r.strip() for r in parts[1].split('/')]

            # 1. Filter out pure number/counter words
            if is_number_word(word):
                filtered_numbers += 1
                continue

            # 2. Get preferred character-by-character reading
            pref_parts = []
            for char in word:
                pref_parts.append(char_map.get(char, char))
            pref_reading = " ".join(pref_parts)
            pref_reading_lower = pref_reading.lower()

            readings_lower = [r.lower() for r in readings]

            # 3. Check if preferred reading matches one of the allowed readings
            if pref_reading_lower in readings_lower:
                # Find the exact casing matching the index
                idx = readings_lower.index(pref_reading_lower)
                final_reading = readings[idx]
                fout.write(f"{word}={final_reading}\n")
                written_count += 1
            else:
                # Fallback to the first reading in the list (or capitalize the preferred char-level reading)
                final_reading = readings[0]
                fout.write(f"{word}={final_reading}\n")
                fallback_count += 1

    print("\n--- CLEANING STATS ---")
    print(f"Total processed: {total_words}")
    print(f"Filtered (numbers/counters): {filtered_numbers}")
    print(f"Cleaned with preferred Hán-Việt: {written_count}")
    print(f"Cleaned with fallback (first match): {fallback_count}")
    print(f"Total output entries: {written_count + fallback_count}")
    print(f"Output saved to {OUTPUT_PATH}")

if __name__ == '__main__':
    clean_dictionary()
