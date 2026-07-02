import os
import subprocess
import argparse
from datasets import load_dataset

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
RAW_DIR = os.path.join(DATA_DIR, 'raw')
EMBEDDINGS_DIR = os.path.join(DATA_DIR, 'embeddings')

def download_thuocl():
    print("Downloading THUOCL dataset...")
    thuocl_dir = os.path.join(RAW_DIR, 'THUOCL')
    if not os.path.exists(thuocl_dir):
        subprocess.run(['git', 'clone', 'https://github.com/thunlp/THUOCL.git', thuocl_dir], check=True)
        print("THUOCL downloaded.")
    else:
        print("THUOCL already exists.")

def download_tatoeba():
    print("Downloading Tatoeba dataset...")
    tatoeba_data = load_dataset("Helsinki-NLP/tatoeba", lang1="en", lang2="zh", split="train", trust_remote_code=True)
    tatoeba_path = os.path.join(RAW_DIR, 'tatoeba.jsonl')
    tatoeba_data.to_json(tatoeba_path, force_ascii=False)
    print(f"Saved Tatoeba to {tatoeba_path}")

def download_opensubtitles():
    print("Downloading OpenSubtitles dataset... (This might take a while)")
    opensub_data = load_dataset("Helsinki-NLP/open_subtitles", lang1="en", lang2="zh_cn", split="train", trust_remote_code=True)
    opensub_path = os.path.join(RAW_DIR, 'opensubtitles.jsonl')
    opensub_data.to_json(opensub_path, force_ascii=False)
    print(f"Saved OpenSubtitles to {opensub_path}")

def download_wmt19():
    print("Downloading WMT19 dataset... (This might take a while)")
    wmt_data = load_dataset("wmt/wmt19", "zh-en", split="train", trust_remote_code=True)
    wmt_path = os.path.join(RAW_DIR, 'wmt19.jsonl')
    wmt_data.to_json(wmt_path, force_ascii=False)
    print(f"Saved WMT19 to {wmt_path}")

def download_tencent_embeddings():
    print("Downloading Tencent AI Lab Embeddings (Conan-embedding-v2)...")
    from huggingface_hub import snapshot_download
    conan_dir = os.path.join(EMBEDDINGS_DIR, 'Conan-embedding-v2')
    os.makedirs(conan_dir, exist_ok=True)
    snapshot_download(repo_id="TencentBAC/Conan-embedding-v2", local_dir=conan_dir)
    print(f"Saved Tencent Embeddings to {conan_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download NLP datasets")
    parser.add_argument('--thuocl', action='store_true', help='Download THUOCL dataset')
    parser.add_argument('--tatoeba', action='store_true', help='Download Tatoeba dataset')
    parser.add_argument('--opensubtitles', action='store_true', help='Download OpenSubtitles dataset')
    parser.add_argument('--wmt19', action='store_true', help='Download WMT19 dataset')
    parser.add_argument('--tencent', action='store_true', help='Download Tencent AI Lab Embeddings')
    parser.add_argument('--all', action='store_true', help='Download all datasets')
    
    args = parser.parse_args()
    
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(EMBEDDINGS_DIR, exist_ok=True)
    
    if args.all or args.thuocl:
        try:
            download_thuocl()
        except Exception as e:
            print(f"Error downloading THUOCL: {e}")
    if args.all or args.tatoeba:
        try:
            download_tatoeba()
        except Exception as e:
            print(f"Error downloading Tatoeba: {e}")
    if args.all or args.opensubtitles:
        try:
            download_opensubtitles()
        except Exception as e:
            print(f"Error downloading OpenSubtitles: {e}")
    if args.all or args.wmt19:
        try:
            download_wmt19()
        except Exception as e:
            print(f"Error downloading WMT19: {e}")
    if args.all or args.tencent:
        try:
            download_tencent_embeddings()
        except Exception as e:
            print(f"Error downloading Tencent AI Lab Embeddings: {e}")
        
    if not any([args.all, args.thuocl, args.tatoeba, args.opensubtitles, args.wmt19, args.tencent]):
        print("Please specify a dataset to download, or use --all.")
        parser.print_help()
