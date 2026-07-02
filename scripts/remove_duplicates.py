import os
import shutil

DICT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dictionaries'))
ALIGNED_PATH = os.path.join(DICT_DIR, 'Aligned_HanViet.txt')
BACKUP_PATH = os.path.join(DICT_DIR, 'Aligned_HanViet.txt.bak3')

def clean_duplicates():
    if not os.path.exists(ALIGNED_PATH):
        print(f"Error: {ALIGNED_PATH} not found.")
        return

    # Backup
    print(f"Creating backup of Aligned_HanViet.txt -> {BACKUP_PATH}")
    shutil.copy2(ALIGNED_PATH, BACKUP_PATH)

    unique_entries = {}
    duplicate_count = 0
    header_lines = []
    total_lines = 0

    with open(ALIGNED_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            total_lines += 1
            stripped = line.strip()
            if line.startswith('#') or not stripped:
                header_lines.append(line)
                continue
            
            parts = stripped.split('=', 1)
            if len(parts) == 2:
                key = parts[0].strip()
                val = parts[1].strip()
                if key in unique_entries:
                    duplicate_count += 1
                    # Keep the one that is capitalized or has more content, or just stick with the first
                    # Let's check if the new one is capitalized and the old one is not:
                    old_val = unique_entries[key]
                    if val != old_val:
                        # If the new one is capitalized (proper name), prefer it
                        if any(c.isupper() for c in val) and not any(c.isupper() for c in old_val):
                            unique_entries[key] = val
                else:
                    unique_entries[key] = val

    print(f"Processed {total_lines:,} lines.")
    print(f"Found {duplicate_count:,} duplicate keys.")

    # Sort the unique entries by key
    sorted_entries = sorted(list(unique_entries.items()), key=lambda x: x[0])
    
    print(f"Writing {len(sorted_entries):,} unique entries back to {ALIGNED_PATH}...")
    
    with open(ALIGNED_PATH, 'w', encoding='utf-8') as f:
        # Write headers
        for h in header_lines:
            f.write(h)
        if not header_lines:
            f.write("# Aligned Hán-Việt dictionary\n")
            f.write("# Format: Chinese_Word=HV_Reading\n\n")
            
        for key, val in sorted_entries:
            f.write(f"{key}={val}\n")
            
    print("Clean duplicates completed successfully!")

if __name__ == '__main__':
    clean_duplicates()
