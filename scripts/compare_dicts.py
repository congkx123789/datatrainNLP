import os

DICT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dictionaries'))
CLEANED_PATH = os.path.join(DICT_DIR, 'missing_compounds_cleaned.txt')
VIETPHRASE_PATH = os.path.join(DICT_DIR, 'Vietphrase.txt')

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
                key = parts[0].strip()
                val = parts[1].strip()
                d[key] = val
    return d

def compare():
    print("Loading missing_compounds_cleaned.txt...")
    cleaned = load_dict(CLEANED_PATH)
    print(f"Loaded {len(cleaned):,} entries.")

    print("Loading Vietphrase.txt...")
    vietphrase = load_dict(VIETPHRASE_PATH)
    print(f"Loaded {len(vietphrase):,} entries.")

    cleaned_keys = set(cleaned.keys())
    vietphrase_keys = set(vietphrase.keys())

    intersection = cleaned_keys.intersection(vietphrase_keys)
    unique_cleaned = cleaned_keys - vietphrase_keys
    unique_vietphrase = vietphrase_keys - cleaned_keys

    print("\n--- KEY OVERLAP STATISTICS ---")
    print(f"Keys in missing_compounds_cleaned.txt: {len(cleaned_keys):,}")
    print(f"Keys in Vietphrase.txt:               {len(vietphrase_keys):,}")
    print(f"Common keys (Intersection):            {len(intersection):,} (Overlap: {len(intersection)/len(cleaned_keys)*100:.2f}% of cleaned, {len(intersection)/len(vietphrase_keys)*100:.2f}% of Vietphrase)")
    print(f"Keys unique to missing_compounds:     {len(unique_cleaned):,}")
    print(f"Keys unique to Vietphrase:             {len(unique_vietphrase):,}")

    # Check translation compatibility in intersection
    match_count = 0
    diff_count = 0
    samples_match = []
    samples_diff = []

    for key in sorted(list(intersection)):
        hv_val = cleaned[key].strip().lower()
        vp_vals = [v.strip().lower() for v in vietphrase[key].split('/')]

        # Check if Hán-Việt reading is one of the translations in Vietphrase
        if hv_val in vp_vals:
            match_count += 1
            if len(samples_match) < 10:
                samples_match.append((key, cleaned[key], vietphrase[key]))
        else:
            diff_count += 1
            if len(samples_diff) < 10:
                samples_diff.append((key, cleaned[key], vietphrase[key]))

    print("\n--- TRANSLATION COMPATIBILITY ON COMMON KEYS ---")
    print(f"Exact matches (HV reading is in Vietphrase): {match_count:,} ({match_count/len(intersection)*100:.2f}%)")
    print(f"Differing translations:                       {diff_count:,} ({diff_count/len(intersection)*100:.2f}%)")

    print("\nSamples where translations MATCH (HV matches Vietphrase):")
    for key, hv, vp in samples_match:
        print(f"  {key}: HV='{hv}' | VP='{vp}'")

    print("\nSamples where translations DIFFER (e.g., Vietphrase is Pure Vietnamese / Semantic):")
    for key, hv, vp in samples_diff:
        print(f"  {key}: HV='{hv}' | VP='{vp}'")

    print("\nSamples unique to missing_compounds_cleaned:")
    for key in sorted(list(unique_cleaned))[:10]:
        print(f"  {key}: HV='{cleaned[key]}'")

    print("\nSamples unique to Vietphrase:")
    for key in sorted(list(unique_vietphrase))[:10]:
        print(f"  {key}: VP='{vietphrase[key]}'")

if __name__ == '__main__':
    compare()
