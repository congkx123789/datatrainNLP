import time
import sys

try:
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    import torch
except ImportError:
    print("Error: Required libraries not found.")
    sys.exit(1)

def main():
    # Use google/t5-efficient-tiny which has exactly ~16.7M parameters
    model_name = "google/t5-efficient-tiny"
    print(f"Loading tiny 17M model '{model_name}' (approx. 60MB)...")
    
    start_load = time.perf_counter()
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    print(f"Model loaded in {time.perf_counter() - start_load:.2f} seconds.")
    
    # Check actual parameters
    num_params = sum(p.numel() for p in model.parameters())
    print(f"Actual model parameters: {num_params:,} ({num_params/1e6:.2f}M)")
    
    # We will simulate translating Chinese to Vietnamese.
    # Note: Since this is a generic pre-trained model (not fine-tuned), it will output random text/gibberish,
    # but the SPEED and execution metrics represent exactly how a 17M parameter translation model would perform.
    test_sentences = [
        "更上一层楼", 
        "民以食为天", 
        "路漫漫其修远兮", 
        "先天下之忧而忧，后天下之乐而乐", 
        "虽然面临许多困难，但我们依然对未来充满信心并正在快速发展。"
    ]
    
    print("\n=======================================================")
    print("      TINY 17M MODEL TRANSLATION BENCHMARK REPORT      ")
    print("=======================================================\n")
    
    for idx, text in enumerate(test_sentences, 1):
        start_tok = time.perf_counter()
        inputs = tokenizer(text, return_tensors="pt")
        tok_time = time.perf_counter() - start_tok
        
        input_len_chars = len(text)
        input_len_tokens = inputs['input_ids'].shape[1]
        
        start_gen = time.perf_counter()
        # Limit max_length to simulate translation generation length
        outputs = model.generate(**inputs, max_length=50)
        gen_time = time.perf_counter() - start_gen
        
        start_dec = time.perf_counter()
        translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        dec_time = time.perf_counter() - start_dec
        
        output_len_chars = len(translated_text)
        output_len_tokens = len(outputs[0])
        
        total_sentence_time = tok_time + gen_time + dec_time
        
        out_tokens_per_sec = output_len_tokens / gen_time if gen_time > 0 else 0
        ms_per_token = (gen_time / output_len_tokens) * 1000 if output_len_tokens > 0 else 0
        
        print(f"[{idx}] CÂU HỎI: {text}")
        print(f"    -> ĐẦU RA (Mô phỏng): {translated_text}")
        print(f"    [Thông số dữ liệu]")
        print(f"      + Input:  {input_len_chars} ký tự | {input_len_tokens} tokens")
        print(f"      + Output: {output_len_chars} ký tự | {output_len_tokens} tokens")
        print(f"    [Thời gian chi tiết]")
        print(f"      + Phân tách từ (Tokenize): {tok_time*1000:.2f} ms")
        print(f"      + Tạo bản dịch (Generation): {gen_time*1000:.2f} ms")
        print(f"      + Giải mã (Decode):        {dec_time*1000:.2f} ms")
        print(f"      + Tổng thời gian:          {total_sentence_time*1000:.2f} ms")
        print(f"    [Hiệu năng dịch thuật]")
        print(f"      + Tốc độ sinh Token:       {out_tokens_per_sec:.2f} tokens/giây")
        print(f"      + Độ trễ mỗi Token:        {ms_per_token:.2f} ms/token")
        print("-" * 55)

if __name__ == "__main__":
    main()
