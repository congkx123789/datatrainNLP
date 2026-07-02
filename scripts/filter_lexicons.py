import os
import requests

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
RAW_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DIR = os.path.join(DATA_DIR, 'processed')

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

def download_file(url, filepath):
    print(f"Downloading {url} to {filepath}...")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("Download complete.")
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def filter_lexicon(input_path, output_path):
    print(f"Filtering {input_path} (length >= 4) -> {output_path}...")
    count = 0
    with open(input_path, 'r', encoding='utf-8') as fin, open(output_path, 'w', encoding='utf-8') as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            
            # Usually dictionaries use space or tab
            delimiter = '\t' if '\t' in line else ' '
            parts = line.split(delimiter)
            
            if parts:
                word = parts[0].strip()
                if len(word) >= 4:
                    fout.write(f"{word}\n")
                    count += 1
                    
    print(f"Filtering complete. Found {count} compound words (length >= 4).")

def process_jieba():
    print("\n--- Processing Jieba Dictionary ---")
    url = "https://raw.githubusercontent.com/fxsjy/jieba/master/jieba/dict.txt"
    raw_path = os.path.join(RAW_DIR, "jieba_dict.txt")
    processed_path = os.path.join(PROCESSED_DIR, "jieba_filtered_4plus.txt")
    
    if not os.path.exists(raw_path):
        success = download_file(url, raw_path)
    else:
        success = True
        
    if success:
        filter_lexicon(raw_path, processed_path)

def process_hanlp():
    print("\n--- Processing HanLP Dictionary ---")
    url = "https://raw.githubusercontent.com/hankcs/HanLP/1.x/data/dictionary/CoreNatureDictionary.txt"
    raw_path = os.path.join(RAW_DIR, "hanlp_dict.txt")
    processed_path = os.path.join(PROCESSED_DIR, "hanlp_filtered_4plus.txt")
    
    if not os.path.exists(raw_path):
        success = download_file(url, raw_path)
    else:
        success = True
        
    if success:
        filter_lexicon(raw_path, processed_path)

def process_ckip():
    print("\n--- Processing CKIP Lexicon ---")
    # CKIP is mostly proprietary or distributed in zips, so we check if the user put it there manually
    raw_path = os.path.join(RAW_DIR, "ckip.txt")
    processed_path = os.path.join(PROCESSED_DIR, "ckip_filtered_4plus.txt")
    
    if os.path.exists(raw_path):
        filter_lexicon(raw_path, processed_path)
    else:
        print(f"Skipping CKIP: Please download the CKIP text file manually and save it as: {raw_path}")
        print("Then run this script again to filter it.")

def process_thuocl():
    print("\n--- Processing THUOCL Dictionaries ---")
    thuocl_dir = os.path.join(RAW_DIR, "THUOCL", "data")
    processed_path = os.path.join(PROCESSED_DIR, "thuocl_filtered_4plus.txt")
    
    if not os.path.exists(thuocl_dir):
        print(f"Skipping THUOCL: Directory not found at {thuocl_dir}")
        return
        
    count = 0
    words = set()
    for filename in os.listdir(thuocl_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(thuocl_dir, filename)
            print(f"Parsing THUOCL file: {filename}...")
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split('\t')
                    if parts:
                        word = parts[0].strip()
                        if len(word) >= 4:
                            words.add(word)
                            
    with open(processed_path, 'w', encoding='utf-8') as fout:
        for word in sorted(words):
            fout.write(f"{word}\n")
            count += 1
            
    print(f"THUOCL processing complete. Found {count} unique compound words (length >= 4).")

if __name__ == "__main__":
    process_jieba()
    process_hanlp()
    process_ckip()
    process_thuocl()
