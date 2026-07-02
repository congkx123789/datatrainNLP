import os
import json
from datasets import load_dataset

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
RAW_DIR = os.path.join(DATA_DIR, 'raw')
os.makedirs(RAW_DIR, exist_ok=True)

def download_tatoeba_zh_vi():
    print("Downloading Tatoeba Chinese-Vietnamese dataset...")
    try:
        # Load Tatoeba Chinese-Vietnamese
        dataset = load_dataset("Helsinki-NLP/tatoeba", lang1="vi", lang2="zh", split="train", trust_remote_code=True)
        out_path = os.path.join(RAW_DIR, "zh_vi_tatoeba.jsonl")
        
        # Save as JSONL: {"zh": "...", "vi": "..."}
        with open(out_path, 'w', encoding='utf-8') as f:
            for item in dataset:
                translation = item.get("translation", {})
                vi_text = translation.get("vi", "").strip()
                zh_text = translation.get("zh", "").strip()
                if vi_text and zh_text:
                    f.write(json.dumps({"zh": zh_text, "vi": vi_text}, ensure_ascii=False) + "\n")
                    
        print(f"Saved Tatoeba (ZH-VI) to {out_path}")
    except Exception as e:
        print(f"Error downloading Tatoeba ZH-VI: {e}")

def download_opensubtitles_zh_vi():
    print("Downloading OpenSubtitles Chinese-Vietnamese dataset (this might take a while)...")
    try:
        # Load OpenSubtitles Chinese-Vietnamese
        dataset = load_dataset("Helsinki-NLP/open_subtitles", lang1="vi", lang2="zh", split="train", trust_remote_code=True)
        out_path = os.path.join(RAW_DIR, "zh_vi_opensubtitles.jsonl")
        
        # Save as JSONL: {"zh": "...", "vi": "..."}
        with open(out_path, 'w', encoding='utf-8') as f:
            for item in dataset:
                translation = item.get("translation", {})
                vi_text = translation.get("vi", "").strip()
                zh_text = translation.get("zh", "").strip()
                if vi_text and zh_text:
                    f.write(json.dumps({"zh": zh_text, "vi": vi_text}, ensure_ascii=False) + "\n")
                    
        print(f"Saved OpenSubtitles (ZH-VI) to {out_path}")
    except Exception as e:
        print(f"Error downloading OpenSubtitles ZH-VI: {e}")

if __name__ == "__main__":
    download_tatoeba_zh_vi()
    # Tatoeba is very fast. We can run OpenSubtitles as well.
    download_opensubtitles_zh_vi()
