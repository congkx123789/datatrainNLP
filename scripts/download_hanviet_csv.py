import os
import requests

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
RAW_DIR = os.path.join(DATA_DIR, 'raw')
os.makedirs(RAW_DIR, exist_ok=True)

def main():
    # Try master branch first, then main branch
    urls = [
        "https://raw.githubusercontent.com/ph0ngp/hanviet-pinyin-wordlist/master/hanviet.csv",
        "https://raw.githubusercontent.com/ph0ngp/hanviet-pinyin-wordlist/main/hanviet.csv"
    ]
    dest_path = os.path.join(RAW_DIR, "hanviet.csv")
    
    success = False
    for url in urls:
        print(f"Trying to download HanViet csv from {url}...")
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"HanViet csv successfully saved to {dest_path}")
            success = True
            break
        except Exception as e:
            print(f"Failed download from {url}: {e}")
            
    if not success:
        print("Could not download the CSV file from any source.")

if __name__ == "__main__":
    main()
