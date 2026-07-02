import os
import re

DICT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dictionaries'))
CLEANED_PATH = os.path.join(DICT_DIR, 'missing_compounds_cleaned.txt')
VIETPHRASE_PATH = os.path.join(DICT_DIR, 'Vietphrase.txt')

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
        'oá': 'óa', 'oà': 'òa', 'oả': 'ỏa', 'oã': 'õa', 'oá': 'óa', 'oạ': 'ọa',
        'uý': 'úy', 'uỳ': 'ùy', 'uỷ': 'ủy', 'uỹ': 'ũy', 'uỵ': 'ụy',
        'oé': 'óe', 'oè': 'òe', 'oẻ': 'ỏe', 'oẽ': 'õe', 'oẹ': 'ọe',
        'uý': 'úy', 'uỳ': 'ùy', 'uỷ': 'ủy', 'uỹ': 'ũy', 'uỵ': 'ụy',
        'uỷ': 'ủy', 'uý': 'úy', 'uỳ': 'ùy', 'uỹ': 'ũy', 'uỵ': 'ụy',
        'uí': 'úy', 'uì': 'ùy', 'uỉ': 'ủy', 'uĩ': 'ũy', 'uị': 'ụy',
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

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

def get_jaccard_similarity(str1, str2):
    w1 = set(str1.split())
    w2 = set(str2.split())
    if not w1 or not w2:
        return 0.0
    return len(w1.intersection(w2)) / len(w1.union(w2))

def analyze_similarity():
    cleaned = load_dict(CLEANED_PATH)
    vietphrase = load_dict(VIETPHRASE_PATH)

    cleaned_keys = set(cleaned.keys())
    vietphrase_keys = set(vietphrase.keys())
    intersection = cleaned_keys.intersection(vietphrase_keys)

    print(f"Comparing {len(intersection):,} common keys...")

    exact_count = 0
    spelling_match_count = 0
    high_sim_count = 0  # Jaccard >= 0.6
    med_sim_count = 0   # 0.3 <= Jaccard < 0.6
    low_sim_count = 0   # Jaccard < 0.3
    
    samples_spelling = []
    samples_high = []
    samples_med = []
    samples_low = []

    for key in sorted(list(intersection)):
        hv_raw = cleaned[key].strip()
        hv_norm = normalize_vietnamese(hv_raw)
        
        vp_raw_list = [v.strip() for v in vietphrase[key].split('/')]
        vp_norm_list = [normalize_vietnamese(v) for v in vp_raw_list]
        
        # 1. Exact match
        if hv_raw.lower() in [v.lower() for v in vp_raw_list]:
            exact_count += 1
            continue
            
        # 2. Spelling difference match (matching after normalization of y/i or tones)
        if hv_norm in vp_norm_list:
            spelling_match_count += 1
            if len(samples_spelling) < 10:
                # Find matching index
                idx = vp_norm_list.index(hv_norm)
                samples_spelling.append((key, hv_raw, vp_raw_list[idx]))
            continue
            
        # 3. Calculate similarities to find highest match
        max_sim = 0.0
        best_vp = ""
        for vp_raw, vp_norm in zip(vp_raw_list, vp_norm_list):
            sim = get_jaccard_similarity(hv_norm, vp_norm)
            if sim > max_sim:
                max_sim = sim
                best_vp = vp_raw
                
        if max_sim >= 0.6:
            high_sim_count += 1
            if len(samples_high) < 10:
                samples_high.append((key, hv_raw, best_vp, max_sim))
        elif max_sim >= 0.3:
            med_sim_count += 1
            if len(samples_med) < 10:
                samples_med.append((key, hv_raw, best_vp, max_sim))
        else:
            low_sim_count += 1
            if len(samples_low) < 10:
                samples_low.append((key, hv_raw, best_vp, max_sim))

    print("\n--- SIMILARITY STATISTICS ---")
    print(f"Total Common Keys: {len(intersection):,}")
    print(f"1. Exact Matches:                       {exact_count:,} ({exact_count/len(intersection)*100:.2f}%)")
    print(f"2. Near Matches (Spelling differences): {spelling_match_count:,} ({spelling_match_count/len(intersection)*100:.2f}%)")
    print(f"3. High Similarity (Jaccard >= 60%):    {high_sim_count:,} ({high_sim_count/len(intersection)*100:.2f}%)")
    print(f"4. Medium Similarity (30% <= J < 60%):  {med_sim_count:,} ({med_sim_count/len(intersection)*100:.2f}%)")
    print(f"5. Low/No Similarity (Jaccard < 30%):   {low_sim_count:,} ({low_sim_count/len(intersection)*100:.2f}%)")
    
    total_closely_aligned = exact_count + spelling_match_count + high_sim_count
    print(f"\n=> Total Closely Aligned (1 + 2 + 3): {total_closely_aligned:,} ({total_closely_aligned/len(intersection)*100:.2f}%)")

    print("\nSamples of SPELLING DIFFERENCES (mostly y/i and tone variants):")
    for key, hv, vp in samples_spelling:
        print(f"  {key}: HV='{hv}' <-> Vietphrase='{vp}'")
        
    print("\nSamples of HIGH SIMILARITY (Jaccard >= 60%):")
    for key, hv, vp, sim in samples_high:
        print(f"  {key}: HV='{hv}' <-> Vietphrase='{vp}' (Sim: {sim*100:.1f}%)")

    print("\nSamples of MEDIUM SIMILARITY (30% <= J < 60%):")
    for key, hv, vp, sim in samples_med:
        print(f"  {key}: HV='{hv}' <-> Vietphrase='{vp}' (Sim: {sim*100:.1f}%)")

    print("\nSamples of LOW SIMILARITY (Jaccard < 30%):")
    for key, hv, vp, sim in samples_low:
        print(f"  {key}: HV='{hv}' <-> Vietphrase='{vp}' (Sim: {sim*100:.1f}%)")

if __name__ == '__main__':
    analyze_similarity()
