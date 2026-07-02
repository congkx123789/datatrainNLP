import os
import re
import shutil

DICT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dictionaries'))
ALIGNED_PATH = os.path.join(DICT_DIR, 'Aligned_HanViet.txt')
CHAR_DICT_PATH = os.path.join(DICT_DIR, 'HanViet_CharDict.txt')
VIETPHRASE_PATH = os.path.join(DICT_DIR, 'Vietphrase.txt')
BACKUP_PATH = os.path.join(DICT_DIR, 'Aligned_HanViet.txt.bak2')

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
                reading = parts[1].strip().lstrip('~')
                if char and reading:
                    char_map[char] = reading
    return char_map

def normalize_vietnamese(text):
    text = text.lower().strip()
    # Normalize y/i variations in common syllables
    text = re.sub(r'\bk[íìỉĩíị]\b', 'ky', text)
    text = re.sub(r'\bl[íìỉĩíị]\b', 'ly', text)
    text = re.sub(r'\bm[íìỉĩíị]\b', 'my', text)
    text = re.sub(r'\bt[íìỉĩíị]\b', 'ty', text)
    text = re.sub(r'\bh[íìỉĩíị]\b', 'hy', text)
    text = re.sub(r'\bs[íìỉĩíị]\b', 'sy', text)
    text = re.sub(r'\b[vđ][íìỉĩíị]\b', lambda m: m.group(0)[0] + 'y', text)
    
    # Normalize tone marks placement
    replacements = {
        'oá': 'óa', 'oà': 'òa', 'oả': 'ỏa', 'oã': 'õa', 'oạ': 'ọa',
        'uý': 'úy', 'uỳ': 'ùy', 'uỷ': 'ủy', 'uỹ': 'ũy', 'uỵ': 'ụy',
        'oé': 'óe', 'oè': 'òe', 'oẻ': 'ỏe', 'oẽ': 'õe', 'oẹ': 'ọe',
        'uí': 'úy', 'uì': 'ùy', 'uỉ': 'ủy', 'uĩ': 'ũy', 'uị': 'ụy',
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def main():
    if not os.path.exists(ALIGNED_PATH):
        print(f"Error: {ALIGNED_PATH} not found.")
        return
        
    # Backup Aligned_HanViet.txt
    print(f"Creating backup of Aligned_HanViet.txt -> {BACKUP_PATH}")
    shutil.copy2(ALIGNED_PATH, BACKUP_PATH)

    char_map = load_char_dict()
    print(f"Loaded {len(char_map)} characters from HanViet_CharDict.txt")

    # Load existing entries in Aligned_HanViet.txt
    existing_entries = []
    existing_keys = set()
    header_lines = []
    
    with open(ALIGNED_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            stripped = line.strip()
            if line.startswith('#') or not stripped:
                header_lines.append(line)
                continue
            parts = stripped.split('=', 1)
            if len(parts) == 2:
                key = parts[0].strip()
                val = parts[1].strip()
                existing_entries.append((key, val))
                existing_keys.add(key)

    print(f"Loaded {len(existing_entries):,} existing entries from Aligned_HanViet.txt")

    if not os.path.exists(VIETPHRASE_PATH):
        print(f"Error: {VIETPHRASE_PATH} not found.")
        return

    new_entries = []
    checked_count = 0
    matched_count = 0

    print("Extracting verified Hán-Việt entries from Vietphrase.txt...")
    with open(VIETPHRASE_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('=', 1)
            if len(parts) != 2:
                continue
            
            word = parts[0].strip()
            # Skip if already in Aligned_HanViet.txt
            if word in existing_keys:
                continue
                
            checked_count += 1
            
            # Compute character-by-character reading
            has_all_chars = True
            pref_parts = []
            for char in word:
                if char in char_map:
                    pref_parts.append(char_map[char])
                else:
                    has_all_chars = False
                    break
            
            if not has_all_chars:
                continue
                
            pref_reading = " ".join(pref_parts)
            pref_reading_norm = normalize_vietnamese(pref_reading)

            # Split Vietphrase translations
            vp_translations = [t.strip() for t in parts[1].split('/')]
            vp_norms = [normalize_vietnamese(t) for t in vp_translations]

            # Check if computed word-to-word reading is in Vietphrase translations
            if pref_reading_norm in vp_norms:
                # Find matching index to preserve casing/spelling from Vietphrase if possible,
                # else fallback to pref_reading
                idx = vp_norms.index(pref_reading_norm)
                matched_val = vp_translations[idx]
                
                # Check casing: if matched_val is not all lowercase, let's keep it.
                # E.g., proper nouns like "Đông Nguỵ".
                new_entries.append((word, matched_val))
                existing_keys.add(word)
                matched_count += 1

    print(f"\nScan complete:")
    print(f" + Checked {checked_count:,} keys from Vietphrase (not in Aligned_HanViet).")
    print(f" + Found {matched_count:,} new verified word-to-word Hán-Việt matches.")
    
    if matched_count > 0:
        # Append new entries sorted
        combined_entries = existing_entries + sorted(new_entries, key=lambda x: x[0])
        print(f"Total entries after merge: {len(combined_entries):,}")
        
        print(f"Writing updated dictionary back to {ALIGNED_PATH}...")
        with open(ALIGNED_PATH, 'w', encoding='utf-8') as f:
            for h in header_lines:
                f.write(h)
            for key, val in combined_entries:
                f.write(f"{key}={val}\n")
        print("Done!")
    else:
        print("No new matches found to merge.")

if __name__ == '__main__':
    main()
