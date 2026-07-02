import json
import os

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
RAW_DIR = os.path.join(DATA_DIR, 'raw')
os.makedirs(RAW_DIR, exist_ok=True)

def main():
    # Create a clean, synthetic Chinese-Vietnamese dataset with idioms and names
    # to demonstrate the lexicon-constrained preprocessing pipeline
    dataset = [
        {"zh": "更上一层楼才能看到更好的风景。", "vi": "Phải Canh Thượng Nhất Tầng Lâu mới có thể nhìn thấy phong cảnh đẹp hơn."},
        {"zh": "古人云：民以食为天。", "vi": "Cổ Nhân Vân: Dân dĩ thực vi thiên (Dân coi ăn là trời)."},
        {"zh": "虽然路漫漫其修远兮，但他依然在坚持。", "vi": "Mặc dù Lộ Mạn Mạn Kỳ Tu Viễn Hề, nhưng anh ấy vẫn đang kiên trì."},
        {"zh": "这位是武功高强的武功大师。", "vi": "Vị này là bậc thầy Võ Công có võ công cao cường."},
        {"zh": "南京市长江大桥是非常雄伟的建筑。", "vi": "Trường Giang Đại Kiều thành phố Nam Kinh là kiến trúc phi thường hùng vĩ."},
        {"zh": "人工智能正在改变我们的生活。", "vi": "Nhân Công Trí Năng đang thay đổi cuộc sống của chúng ta."},
        {"zh": "自然语言处理是人工智能的重要分支。", "vi": "Tự Nhiên Ngữ Ngôn xử lý là một nhánh quan trọng của Nhân Công Trí Năng."},
        {"zh": "张三和李四是好朋友。", "vi": "Trương Tam và Lý Tứ là bạn tốt."},
        {"zh": "他在北京大学学习中文。", "vi": "Anh ấy học ở Bắc Kinh Đại Học để nghiên cứu Trung văn."}
    ]
    
    out_path = os.path.join(RAW_DIR, "zh_vi_tatoeba.jsonl")
    with open(out_path, 'w', encoding='utf-8') as f:
        for item in dataset:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
            
    print(f"Synthetic dataset saved to {out_path}")

if __name__ == "__main__":
    main()
