import os
import time
import subprocess
import sys

# Ensure output directories exist
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
RAW_DIR = os.path.join(DATA_DIR, 'raw')
CT2_DIR = os.path.join(DATA_DIR, 'ct2_models')
os.makedirs(CT2_DIR, exist_ok=True)

try:
    import ctranslate2
    from transformers import AutoTokenizer
except ImportError:
    print("Error: Required libraries (ctranslate2, transformers) not found. Please wait for pip installation to complete.")
    sys.exit(1)

def convert_model(model_name, output_name, quantization="int8"):
    output_path = os.path.join(CT2_DIR, output_name)
    if os.path.exists(output_path):
        print(f"Model {model_name} already converted at {output_path}")
        return output_path
        
    print(f"\n--- Converting {model_name} to CTranslate2 ({quantization}) ---")
    cmd = [
        "ct2-transformers-converter",
        "--model", model_name,
        "--output_dir", output_path,
        "--quantization", quantization,
        "--force"
    ]
    try:
        subprocess.run(cmd, check=True)
        print("Conversion complete!")
        return output_path
    except Exception as e:
        print(f"Failed to convert model: {e}")
        return None

def benchmark_ct2_t5(model_path, tokenizer_name, test_sentences):
    print(f"\nBenchmark T5 17M with CTranslate2 INT8 on CPU:")
    # For T5, we use ctranslate2.Translator
    translator = ctranslate2.Translator(model_path, device="cpu")
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    
    print("\n--- Running Translations ---")
    total_time = 0
    total_tokens = 0
    
    for idx, text in enumerate(test_sentences, 1):
        start_time = time.perf_counter()
        
        # Tokenize
        input_tokens = tokenizer.convert_ids_to_tokens(tokenizer.encode(text))
        
        # Translate (force min 20 tokens to measure real speed since it's a raw un-finetuned model)
        results = translator.translate_batch([input_tokens], min_decoding_length=20, max_decoding_length=20)
        output_tokens = results[0].hypotheses[0]
        
        # Decode
        translated_text = tokenizer.decode(tokenizer.convert_tokens_to_ids(output_tokens), skip_special_tokens=True)
        
        elapsed = time.perf_counter() - start_time
        total_time += elapsed
        total_tokens += len(output_tokens)
        
        print(f"[{idx}] Gốc: {text}")
        print(f"    Dịch: {translated_text}")
        print(f"    Thời gian: {elapsed*1000:.2f} ms | Số token sinh ra: {len(output_tokens)}")
        print(f"    Tốc độ: {len(output_tokens)/elapsed:.2f} tokens/giây\n")
        
    print(f"Kết quả T5 17M: Tốc độ TB = {total_tokens/total_time:.2f} tokens/giây | Độ trễ TB = {(total_time/len(test_sentences))*1000:.2f} ms/câu")

def benchmark_ct2_marian(model_path, tokenizer_name, test_sentences):
    print(f"\nBenchmark OPUS-MT 74M with CTranslate2 INT8 on CPU:")
    translator = ctranslate2.Translator(model_path, device="cpu")
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    
    print("\n--- Running Translations ---")
    total_time = 0
    total_tokens = 0
    
    for idx, text in enumerate(test_sentences, 1):
        start_time = time.perf_counter()
        
        # Tokenize (Marian models require target prefix usually, but Helsinki-NLP doesn't mandate it if it's 1-to-1)
        input_tokens = tokenizer.convert_ids_to_tokens(tokenizer.encode(text))
        
        # Translate
        results = translator.translate_batch([input_tokens])
        output_tokens = results[0].hypotheses[0]
        
        # Decode
        translated_text = tokenizer.decode(tokenizer.convert_tokens_to_ids(output_tokens), skip_special_tokens=True)
        
        elapsed = time.perf_counter() - start_time
        total_time += elapsed
        total_tokens += len(output_tokens)
        
        print(f"[{idx}] Gốc: {text}")
        print(f"    Dịch: {translated_text}")
        print(f"    Thời gian: {elapsed*1000:.2f} ms | Số token sinh ra: {len(output_tokens)}")
        print(f"    Tốc độ: {len(output_tokens)/elapsed:.2f} tokens/giây\n")
        
    print(f"Kết quả OPUS 74M: Tốc độ TB = {total_tokens/total_time:.2f} tokens/giây | Độ trễ TB = {(total_time/len(test_sentences))*1000:.2f} ms/câu")


if __name__ == "__main__":
    test_sentences = [
        "更上一层楼", 
        "民以食为天", 
        "路漫漫其修远兮", 
        "先天下之忧而忧，后天下之乐而乐", 
        "虽然面临许多困难，但我们依然对未来充满信心并正在快速发展。"
    ]
    
    # 1. Optimize and benchmark T5 (17M)
    t5_ct2_path = convert_model("google/t5-efficient-tiny", "t5_tiny_int8", quantization="int8")
    if t5_ct2_path:
        benchmark_ct2_t5(t5_ct2_path, "google/t5-efficient-tiny", test_sentences)
        
    print("=" * 60)
        
    # 2. Optimize and benchmark OPUS-MT (74M)
    opus_ct2_path = convert_model("Helsinki-NLP/opus-mt-zh-vi", "opus_zh_vi_int8", quantization="int8")
    if opus_ct2_path:
        benchmark_ct2_marian(opus_ct2_path, "Helsinki-NLP/opus-mt-zh-vi", test_sentences)
