import time
import os
import sys

try:
    import jieba
    import jieba.posseg as pseg
except ImportError:
    print("Error: 'jieba' library not found.")
    sys.exit(1)

def main():
    poem_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'THUOCL', 'data', 'THUOCL_poem.txt'))
    if not os.path.exists(poem_file):
        print(f"Error: Poem file not found at {poem_file}")
        sys.exit(1)
        
    print("Initializing Jieba...")
    jieba.initialize()
    
    # Read first 2000 lines from THUOCL_poem.txt to make a robust benchmark
    sentences = []
    with open(poem_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # THUOCL format: word \t freq. We only need the word.
            parts = line.split('\t')
            sentences.append(parts[0])
            if len(sentences) >= 2000:
                break
                
    print(f"Loaded {len(sentences)} idioms/poems for benchmarking.")
    
    # Warm up
    pseg.lcut("测试热身")
    
    print("\n--- Running Large-Scale Benchmark ---")
    start_time = time.perf_counter()
    
    total_chars = 0
    total_words = 0
    
    for text in sentences:
        words = pseg.lcut(text)  # Use lcut to return a list and force evaluation
        total_words += len(words)
        total_chars += len(text)
        
    elapsed = time.perf_counter() - start_time
    
    print("\n=======================================================")
    print("         JIEBA SUSTAINED SPEED REPORT                  ")
    print("=======================================================")
    print(f" + Số câu xử lý:          {len(sentences):,} câu")
    print(f" + Tổng số ký tự (Chữ):    {total_chars:,} ký tự Hán")
    print(f" + Tổng số từ được tách:   {total_words:,} từ")
    print(f" + Thời gian xử lý:        {elapsed:.4f} giây ({elapsed*1000:.2f} ms)")
    print(f" + Tốc độ dịch/phân loại:   {total_chars / elapsed:.2f} ký tự/giây")
    print(f" + Thời gian trung bình:    {(elapsed / len(sentences))*1000:.4f} ms/câu")
    print("=======================================================")

if __name__ == "__main__":
    main()
