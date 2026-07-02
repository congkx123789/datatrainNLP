import os

DICT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dictionaries'))
VIETPHRASE_PATH = os.path.join(DICT_DIR, 'Vietphrase.txt')

def analyze():
    if not os.path.exists(VIETPHRASE_PATH):
        print(f"Error: {VIETPHRASE_PATH} not found.")
        return

    total_entries = 0
    by_len = {}
    multiple_translations = 0
    total_translations = 0
    max_translations = 0
    max_trans_phrase = ""
    max_trans_list = []
    
    sample_by_len = {}

    with open(VIETPHRASE_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            parts = line.split('=', 1)
            if len(parts) != 2:
                continue
            
            total_entries += 1
            zh_phrase = parts[0].strip()
            vi_translations = [t.strip() for t in parts[1].split('/')]
            num_trans = len(vi_translations)
            
            total_translations += num_trans
            if num_trans > 1:
                multiple_translations += 1
            if num_trans > max_translations:
                max_translations = num_trans
                max_trans_phrase = zh_phrase
                max_trans_list = vi_translations
            
            length = len(zh_phrase)
            by_len[length] = by_len.get(length, 0) + 1
            
            if length not in sample_by_len and len(sample_by_len) < 15:
                # Store sample
                sample_by_len[length] = (zh_phrase, vi_translations)

    print("\n--- VIETPHRASE ANALYSIS RESULTS ---")
    print(f"Total entries: {total_entries:,}")
    print(f"Average translations per phrase: {total_translations / total_entries:.2f}")
    print(f"Entries with multiple translations: {multiple_translations:,} ({multiple_translations / total_entries * 100:.2f}%)")
    print(f"Phrase with most translations: '{max_trans_phrase}' ({max_readings} -> {max_translations} translations)")
    print(f"Example translations of '{max_trans_phrase}': {max_trans_list[:5]} ...")
    
    print("\nDistribution of Chinese phrase lengths (in characters):")
    for length in sorted(by_len.keys()):
        count = by_len[length]
        pct = (count / total_entries) * 100
        if pct > 0.1 or length <= 5:
            print(f"  Length {length}: {count:,} ({pct:.2f}%)")
            
    print("\nSamples by length:")
    for length in sorted(sample_by_len.keys())[:10]:
        zh, vi = sample_by_len[length]
        print(f"  Length {length}: {zh} -> {vi}")

if __name__ == '__main__':
    # Define max_readings dummy just in case
    max_readings = 0
    analyze()
