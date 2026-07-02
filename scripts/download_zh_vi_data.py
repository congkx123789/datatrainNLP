import os
import json
from datasets import load_dataset

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
RAW_DIR = os.path.join(DATA_DIR, 'raw')
os.makedirs(RAW_DIR, exist_ok=True)

def download_tatoeba_zh_vi():
    print("Downloading Tatoeba Chinese-Vietnamese dataset...")
    try:
        # Load Tatoeba Chinese-Vietnamese using tatoeba_mt as a working fallback
        dataset = load_dataset("Helsinki-NLP/tatoeba_mt", "vie-zho", split="test", trust_remote_code=True)
        out_path = os.path.join(RAW_DIR, "zh_vi_tatoeba.jsonl")
        
        # Save as JSONL: {"zh": "...", "vi": "..."}
        with open(out_path, 'w', encoding='utf-8') as f:
            for item in dataset:
                vi_text = item.get("sourceString", "").strip()
                zh_text = item.get("targetString", "").strip()
                if vi_text and zh_text:
                    f.write(json.dumps({"zh": zh_text, "vi": vi_text}, ensure_ascii=False) + "\n")
                    
        print(f"Saved Tatoeba (ZH-VI) to {out_path}")
    except Exception as e:
        print(f"Error downloading Tatoeba ZH-VI: {e}")

def download_opensubtitles_zh_vi():
    print("Downloading OpenSubtitles Chinese-Vietnamese dataset (using nlp_data_zh_vi fallback)...")
    try:
        # Load manhha2502/nlp_data_zh_vi as an alternative to the broken OpenSubtitles ZH-VI link
        dataset = load_dataset("manhha2502/nlp_data_zh_vi", split="train", trust_remote_code=True)
        out_path = os.path.join(RAW_DIR, "zh_vi_opensubtitles.jsonl")
        
        # Save as JSONL: {"zh": "...", "vi": "..."}
        with open(out_path, 'w', encoding='utf-8') as f:
            for item in dataset:
                zh_text = item.get("src_lang", "").strip()
                vi_text = item.get("tgt_lang", "").strip()
                if vi_text and zh_text:
                    f.write(json.dumps({"zh": zh_text, "vi": vi_text}, ensure_ascii=False) + "\n")
                    
        print(f"Saved OpenSubtitles (ZH-VI) to {out_path}")
    except Exception as e:
        print(f"Error downloading OpenSubtitles ZH-VI: {e}")

if __name__ == "__main__":
    download_tatoeba_zh_vi()
    # Tatoeba is very fast. We can run OpenSubtitles as well.
    download_opensubtitles_zh_vi()
