import os
import csv
import ast
import zhconv

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
RAW_DIR = os.path.join(DATA_DIR, 'raw')
CSV_PATH = os.path.join(RAW_DIR, "hanviet.csv")

class HanVietConverter:
    def __init__(self):
        self.char_map = {}
        self.load_dictionary()

    def load_dictionary(self):
        if not os.path.exists(CSV_PATH):
            print(f"Error: {CSV_PATH} not found.")
            return

        with open(CSV_PATH, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            # Skip header
            next(reader, None)
            
            for row in reader:
                if len(row) < 2:
                    continue
                char = row[0]
                hanviet_str = row[1]
                
                try:
                    hanviet_list = ast.literal_eval(hanviet_str)
                except Exception:
                    hanviet_list = [hanviet_str.replace("[", "").replace("]", "").replace("'", "").strip()]
                
                if char not in self.char_map:
                    self.char_map[char] = hanviet_list[0] if hanviet_list else ""

    def convert_char(self, char):
        # Convert Simplified to Traditional Chinese first
        trad_char = zhconv.convert(char, 'zh-hant')
        return self.char_map.get(trad_char, char)

    def convert_word(self, word):
        converted = []
        for char in word:
            converted.append(self.convert_char(char).capitalize())
        return " ".join(converted)

if __name__ == "__main__":
    converter = HanVietConverter()
    # Test some samples
    test_words = ["南京市", "人工智能", "自然语言", "武功", "更上一层楼"]
    for w in test_words:
        print(f"ZH: {w} -> HV: {converter.convert_word(w)}")
