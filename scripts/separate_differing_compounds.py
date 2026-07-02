import os
import re
import shutil

DICT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dictionaries'))
ALIGNED_PATH = os.path.join(DICT_DIR, 'Aligned_HanViet.txt')
VIETPHRASE_PATH = os.path.join(DICT_DIR, 'Vietphrase.txt')
DIFFERING_PATH = os.path.join(DICT_DIR, 'Aligned_HanViet_Differing.txt')
ORIGINAL_BACKUP = os.path.join(DICT_DIR, 'Aligned_HanViet.txt.bak') # Original backup before any changes

# If original backup doesn't exist, we will try to look for bak2 or bak3
if not os.path.exists(ORIGINAL_BACKUP):
    print("Warning: Aligned_HanViet.txt.bak not found. Trying to recover from git or bak2/bak3.")

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

def load_keys(filepath):
    keys = set()
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        return keys
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('=', 1)
            if len(parts) == 2:
                keys.add(parts[0].strip())
    return keys

def load_dict(filepath):
    d = {}
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        return d
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('=', 1)
            if len(parts) == 2:
                d[parts[0].strip()] = parts[1].strip()
    return d

def separate():
    # 1. Load original Aligned_HanViet.txt keys
    original_keys = set()
    if os.path.exists(ORIGINAL_BACKUP):
        original_keys = load_keys(ORIGINAL_BACKUP)
        print(f"Loaded {len(original_keys):,} original keys from {ORIGINAL_BACKUP}")
    else:
        print("Error: Cannot proceed without the original backup Aligned_HanViet.txt.bak to distinguish original keys.")
        return

    # 2. Load Vietphrase translations
    print("Loading Vietphrase.txt...")
    vietphrase = load_dict(VIETPHRASE_PATH)
    print(f"Loaded {len(vietphrase):,} Vietphrase entries.")

    # 3. Load current Aligned_HanViet.txt entries
    print("Loading current Aligned_HanViet.txt...")
    current_entries = []
    header_lines = []
    
    with open(ALIGNED_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            stripped = line.strip()
            if line.startswith('#') or not stripped:
                header_lines.append(line)
                continue
            parts = stripped.split('=', 1)
            if len(parts) == 2:
                current_entries.append((parts[0].strip(), parts[1].strip()))

    print(f"Loaded {len(current_entries):,} entries from current Aligned_HanViet.txt")

    kept_entries = []
    differing_entries = []

    for key, val in current_entries:
        # If it is in the original dictionary, we keep it
        if key in original_keys:
            kept_entries.append((key, val))
            continue

        # If it is not in the original dictionary, we check if it matches Vietphrase
        if key in vietphrase:
            hv_norm = normalize_vietnamese(val)
            vp_translations = [t.strip() for t in vietphrase[key].split('/')]
            vp_norms = [normalize_vietnamese(t) for t in vp_translations]
            
            if hv_norm in vp_norms:
                # It is an exact or near spelling match, so keep it!
                kept_entries.append((key, val))
            else:
                # It is a differing translation (High, Medium, or Low similarity), move it!
                differing_entries.append((key, val))
        else:
            # If it is not in Vietphrase, it must have come from clean missing compounds,
            # but since we only merged the intersection keys, it should be in Vietphrase.
            # Just in case, keep it.
            kept_entries.append((key, val))

    print("\n--- SEPARATION STATISTICS ---")
    print(f"Total entries processed: {len(current_entries):,}")
    print(f"Entries kept in Aligned_HanViet.txt: {len(kept_entries):,}")
    print(f"Entries moved to Aligned_HanViet_Differing.txt: {len(differing_entries):,}")

    # Write kept entries back to Aligned_HanViet.txt
    print(f"\nWriting kept entries back to {ALIGNED_PATH}...")
    with open(ALIGNED_PATH, 'w', encoding='utf-8') as f:
        for h in header_lines:
            f.write(h)
        for key, val in sorted(kept_entries, key=lambda x: x[0]):
            f.write(f"{key}={val}\n")

    # Write differing entries to Aligned_HanViet_Differing.txt
    print(f"Writing differing entries to {DIFFERING_PATH}...")
    with open(DIFFERING_PATH, 'w', encoding='utf-8') as f:
        fout_headers = [
            "# Aligned Hán-Việt dictionary containing differing translations\n",
            "# These entries are from the intersection of missing compounds and Vietphrase but have differing translations\n",
            "# Format: Chinese_Word=HV_Reading\n\n"
        ]
        for h in fout_headers:
            f.write(h)
        for key, val in sorted(differing_entries, key=lambda x: x[0]):
            f.write(f"{key}={val}\n")

    print("Separation completed successfully!")

if __name__ == '__main__':
    separate()
