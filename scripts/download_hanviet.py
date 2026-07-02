import os
import requests

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
RAW_DIR = os.path.join(DATA_DIR, 'raw')
os.makedirs(RAW_DIR, exist_ok=True)

def main():
    # VietPhrase repository HanViet dictionary raw URL
    url = "https://raw.githubusercontent.com/ryanphung/chinese-hanviet-cognates/master/data/phienam.txt"
    dest_path = os.path.join(RAW_DIR, "HanViet.txt")
    
    print(f"Downloading HanViet dictionary from {url}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        with open(dest_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"HanViet dictionary successfully saved to {dest_path}")
    except Exception as e:
        print(f"Error downloading dictionary: {e}")

if __name__ == "__main__":
    main()
