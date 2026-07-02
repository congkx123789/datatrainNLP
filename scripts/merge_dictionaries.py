import os
import shutil

DICT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dictionaries'))
ALIGNED_PATH = os.path.join(DICT_DIR, 'Aligned_HanViet.txt')
CLEANED_PATH = os.path.join(DICT_DIR, 'missing_compounds_cleaned.txt')
VIETPHRASE_PATH = os.path.join(DICT_DIR, 'Vietphrase.txt')
BACKUP_PATH = os.path.join(DICT_DIR, 'Aligned_HanViet.txt.bak')

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

def merge():
    # 1. Backup original Aligned_HanViet.txt
    if os.path.exists(ALIGNED_PATH):
        print(f"Creating backup of Aligned_HanViet.txt -> {BACKUP_PATH}")
        shutil.copy2(ALIGNED_PATH, BACKUP_PATH)
    else:
        print("Error: Aligned_HanViet.txt not found. Cannot merge.")
        return

    # 2. Load existing entries in Aligned_HanViet.txt
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

    # 3. Load keys of clean missing compounds and Vietphrase
    print("Loading keys from missing_compounds_cleaned.txt...")
    cleaned_dict = load_dict(CLEANED_PATH)
    cleaned_keys = set(cleaned_dict.keys())
    print(f"Loaded {len(cleaned_keys):,} keys.")

    print("Loading keys from Vietphrase.txt...")
    vietphrase_keys = load_keys(VIETPHRASE_PATH)
    print(f"Loaded {len(vietphrase_keys):,} keys.")

    # 4. Find the intersection (overlap)
    intersection = cleaned_keys.intersection(vietphrase_keys)
    print(f"Found {len(intersection):,} keys in the intersection.")

    # 5. Filter out keys that are already in Aligned_HanViet.txt (just in case)
    new_keys = intersection - existing_keys
    print(f"{len(new_keys):,} of these intersecting keys are new to Aligned_HanViet.txt")

    # 6. Add new entries
    new_entries = []
    for key in sorted(list(new_keys)):
        new_entries.append((key, cleaned_dict[key]))

    # Combine existing and new entries
    combined_entries = existing_entries + new_entries
    print(f"Total entries after merge: {len(combined_entries):,}")

    # 7. Write back to Aligned_HanViet.txt
    print(f"Writing merged dictionary to {ALIGNED_PATH}...")
    with open(ALIGNED_PATH, 'w', encoding='utf-8') as f:
        # Write headers
        for h in header_lines:
            f.write(h)
        if not header_lines:
            f.write("# Aligned Hán-Việt dictionary created from enriched dictionaries & Vietnamese corpora\n")
            f.write("# Format: Chinese_Word=HV_Reading1/HV_Reading2/...\n\n")
            
        # Write all combined entries
        for key, val in combined_entries:
            f.write(f"{key}={val}\n")

    print("Merge successfully completed!")

if __name__ == '__main__':
    merge()
