import time
import sys

try:
    import jieba
    import jieba.posseg as pseg
except ImportError:
    print("Error: 'jieba' library not found. Please wait for pip install to finish.")
    sys.exit(1)

def main():
    print("Initializing Jieba POS Tagger (Loading dictionary)...")
    start_init = time.perf_counter()
    # Force initialize Jieba
    jieba.initialize()
    print(f"Jieba initialized in {time.perf_counter() - start_init:.2f} seconds.")
    
    test_sentences = [
        "更上一层楼", 
        "民以食为天", 
        "路漫漫其修远兮", 
        "先天下之忧而忧，后天下之乐而乐", 
        "虽然面临许多困难，但我们依然对未来充满信心并正在快速发展。"
    ]
    
    print("\n=======================================================")
    print("      JIEBA PART-OF-SPEECH (POS) TAGGING BENCHMARK     ")
    print("=======================================================\n")
    
    total_time = 0
    total_chars = 0
    
    for idx, text in enumerate(test_sentences, 1):
        start_time = time.perf_counter()
        
        # Run POS Tagging
        words = pseg.cut(text)
        result = [(word, flag) for word, flag in words]
        
        elapsed = time.perf_counter() - start_time
        total_time += elapsed
        total_chars += len(text)
        
        # Format output
        formatted_result = " | ".join([f"{w}({t})" for w, t in result])
        
        print(f"[{idx}] CÂU GỐC: {text}")
        print(f"    -> PHÂN LOẠI: {formatted_result}")
        print(f"    Thời gian xử lý: {elapsed*1000:.3f} ms")
        print("-" * 55)
        
    print(f"Tổng số ký tự xử lý: {total_chars} ký tự.")
    print(f"Tổng thời gian xử lý: {total_time*1000:.3f} ms.")
    print(f"Tốc độ trung bình: {total_chars / total_time:.2f} ký tự/giây.")

if __name__ == "__main__":
    main()
