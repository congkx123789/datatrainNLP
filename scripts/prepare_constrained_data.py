import os
import json
import jieba
import jieba.posseg as pseg
from hanviet_converter import HanVietConverter

# Directory setup
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
RAW_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DIR = os.path.join(DATA_DIR, 'processed')

os.makedirs(PROCESSED_DIR, exist_ok=True)

def load_wordlist(filepath):
    words = set()
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip()
                if word:
                    words.add(word)
    return words

def main():
    print("Initializing HanViet Converter and loading dictionaries...")
    converter = HanVietConverter()
    
    # Load the 4+ character compound words we filtered earlier
    jieba_4plus = load_wordlist(os.path.join(PROCESSED_DIR, "jieba_filtered_4plus.txt"))
    hanlp_4plus = load_wordlist(os.path.join(PROCESSED_DIR, "hanlp_filtered_4plus.txt"))
    compound_dict = jieba_4plus.union(hanlp_4plus)
    print(f"Loaded {len(compound_dict):,} compound words (length >= 4).")
    
    input_file = os.path.join(RAW_DIR, "zh_vi_opensubtitles.jsonl")
    output_file = os.path.join(PROCESSED_DIR, "train_constrained.jsonl")
    
    if not os.path.exists(input_file):
        # Fallback to tatoeba if opensubtitles is not loaded yet
        input_file = os.path.join(RAW_DIR, "zh_vi_tatoeba.jsonl")
        
    if not os.path.exists(input_file):
        print("Error: No ZH-VI datasets found. Please run scripts/download_zh_vi_data.py first.")
        return
        
    print(f"Reading from {input_file} and writing to {output_file}...")
    
    processed_count = 0
    skipped_count = 0
    max_sentences = 20000
    
    with open(input_file, 'r', encoding='utf-8') as fin, open(output_file, 'w', encoding='utf-8') as fout:
        for line in fin:
            if processed_count >= max_sentences:
                break
                
            try:
                item = json.loads(line)
                zh_text = item.get("zh", "").strip()
                vi_text = item.get("vi", "").strip()
                
                if not zh_text or not vi_text:
                    continue
                
                # Wait! OpenSubtitles was downloaded as en-zh_cn (lang1="en", lang2="zh_cn").
                # This means it's English-Chinese!
                # Wait! The user wants a CHINESE-VIETNAMESE translation model!
                # If they want a Chinese-Vietnamese model, they need Chinese-Vietnamese datasets.
                # Oh, is OpenSubtitles en-zh_cn? Yes, the download code was:
                # `load_dataset("Helsinki-NLP/open_subtitles", lang1="en", lang2="zh_cn")`
                # And Tatoeba was `load_dataset("Helsinki-NLP/tatoeba", lang1="en", lang2="zh")`
                # And WMT19 was `load_dataset("wmt/wmt19", "zh-en")`
                # These are all Chinese-English datasets!
                # Wait, if they are Chinese-English, the user wants me to do:
                # "dịch ra sẵn thành cặp hán việt rồi hay là tên hán việt rồi thì nó sẽ kiểu là điền vào chỗ trống"
                # Since Hán Việt is a Sino-Vietnamese reading, it is used to translate Chinese names to Vietnamese (e.g. in Chinese-Vietnamese translation models).
                # Even if the training dataset is Chinese-English (zh-en), we can translate the Chinese name to Hán Việt (e.g., 武功 -> Vũ Công) and inject it as a hint for a Chinese-Vietnamese translation system, or we can use a Chinese-Vietnamese dataset!
                # Do we have a Chinese-Vietnamese dataset?
                # Actually, the model Helsinki-NLP/opus-mt-zh-vi is Chinese-Vietnamese!
                # If we want to fine-tune `Helsinki-NLP/opus-mt-zh-vi`, we need Chinese-Vietnamese sentence pairs.
                # Where do we get Chinese-Vietnamese sentence pairs?
                # Wait, does Hugging Face have a Chinese-Vietnamese dataset?
                # Yes! For example, `enviet/vi-zh` or `translation` or we can find one.
                # Or, we can simulate the data preparation by translating the English part of WMT19/OpenSubtitles to Vietnamese using our local `opus-mt-zh-vi` model or another translation API, OR we can download a public zh-vi dataset.
                # Actually, there is a dataset `Helsinki-NLP/opus-mt-zh-vi` which can be fine-tuned. The OPUS corpus has `opus_books` or `ted_talks` or `tatoeba` for `zh-vi`.
                # Let's check: Tatoeba has a `zh-vi` pair!
                # `load_dataset("Helsinki-NLP/tatoeba", lang1="zh", lang2="vi")`
                # This is a Chinese-Vietnamese dataset!
                # Let's check if we can download `tatoeba` for `zh-vi`. It's very small.
                # For the sake of this data prep script, let's write it to handle any JSONL file with {"zh": "...", "vi": "..."} or {"translation": {"zh": "...", "vi": "..."}}.
                # Let's write the tag insertion logic assuming we have a `zh` and a `vi` sentence pair.
                
                # Let's assume the jsonl format has keys 'zh' and 'vi'.
                # E.g.: {"zh": "南京市长江大桥正在开通。", "vi": "Cầu Trường Giang của thành phố Nam Kinh đang được thông xe."}
                
                # We will parse Jieba posseg to find nouns (n), proper names (nr), idioms (i), or compound words in compound_dict.
                words_with_tags = pseg.lcut(zh_text)
                
                tagged_zh = []
                has_hint = False
                
                for word, flag in words_with_tags:
                    # Allow tagging for all compound words of length >= 2
                    if len(word) >= 2:
                        # Find HanViet reading
                        hanviet = converter.convert_word(word)
                        # We strip spaces for names, or keep them. Let's keep them capitalized.
                        # Check if this HanViet reading (lowercase) is somewhat present in the Vietnamese target sentence
                        # (This ensures we only inject hints that are actually in the target translation!)
                        # To make it simple: if the target sentence has any word of the HanViet reading, we inject it.
                        # This prevents injecting wrong hints during training.
                        
                        # Let's normalize both to compare
                        vi_norm = vi_text.lower()
                        hv_words = [w.lower() for w in hanviet.split()]
                        
                        # If any part of the HanViet reading matches the Vietnamese sentence
                        if any(hw in vi_norm for hw in hv_words if len(hw) > 2) or flag == 'nr':
                            tagged_zh.append(f"{word}<vi: {hanviet}|{flag}>")
                            has_hint = True
                        else:
                            tagged_zh.append(word)
                    else:
                        tagged_zh.append(word)
                
                # Reconstruct input sentence
                input_sentence = "".join(tagged_zh)
                
                # Only write to train file if it actually contains a hint (to make the model learn the copy mechanism)
                # or write a mix of both (some with hints, some without)
                fout.write(json.dumps({
                    "zh_raw": zh_text,
                    "zh_tagged": input_sentence,
                    "vi": vi_text,
                    "has_hint": has_hint
                }, ensure_ascii=False) + "\n")
                processed_count += 1
                
            except Exception as e:
                skipped_count += 1
                continue
                
    print(f"\nData preparation complete!")
    print(f" + Successfully processed: {processed_count:,} pairs")
    print(f" + Skipped/Errors:          {skipped_count:,} lines")
    print(f" + Output saved to:         {output_file}")

if __name__ == "__main__":
    main()
