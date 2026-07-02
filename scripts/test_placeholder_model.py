import os
import torch
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Constants
MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'constrained_mt_model'))

def test_placeholder_translation():
    if not os.path.exists(MODEL_DIR):
        print(f"Fine-tuned model not found at {MODEL_DIR}. Please run scripts/train_tiny.py first.")
        return

    print(f"Loading fine-tuned placeholder model from {MODEL_DIR}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_DIR)
    model.eval()

    # Define test sentences with placeholders and their corresponding dictionaries
    test_cases = [
        {
            "zh_tagged": "张三<1|nr>和李四<2|nr>是好朋友。",
            "dict": {
                "<1>": "Trương Tam",
                "<2>": "Lý Tứ"
            }
        },
        {
            "zh_tagged": "武功<1|nr>和李四<2|nr>是好朋友。",
            "dict": {
                "<1>": "Võ Công",
                "<2>": "Lý Tứ"
            }
        },
        {
            "zh_tagged": "张三<1|nr>去南京市<2|ns>。",
            "dict": {
                "<1>": "Trương Tam",
                "<2>": "Nam Kinh Thị"
            }
        },
        {
            "zh_tagged": "南京市<1|ns>长江大桥<2|ns>是非常<3|d>雄伟<4|a>的建筑<5|n>。",
            "dict": {
                "<1>": "Nam Kinh Thị",
                "<2>": "Trường Giang Đại Kiều",
                "<3>": "Phi Thường",
                "<4>": "Hùng Vĩ",
                "<5>": "Kiến Trúc"
            }
        },
        {
            "zh_tagged": "她在北京大学<1|nt>学习人工智能<2|n>。",
            "dict": {
                "<1>": "Bắc Kinh Đại Học",
                "<2>": "Nhân Công Trí Năng"
            }
        },
        {
            "zh_tagged": "他是好朋友<1|n>。",
            "dict": {
                "<1>": "Hảo Bằng Hữu"
            }
        },
        # A test case to demonstrate ANY arbitrary text can be copy-pasted
        {
            "zh_tagged": "他是好朋友<1|n>。",
            "dict": {
                "<1>": "abcxyz_arbitrary_string"
            }
        }
    ]

    print("\n" + "="*50)
    print("RUNNING PLACEHOLDER-BASED TRANSLATION TESTS")
    print("="*50)

    for idx, case in enumerate(test_cases, 1):
        zh_input = case["zh_tagged"]
        mapping_dict = case["dict"]
        
        # Tokenize input
        inputs = tokenizer(zh_input, return_tensors="pt")
        
        # Generate raw translation
        with torch.no_grad():
            outputs = model.generate(**inputs, max_length=128, num_beams=4, early_stopping=True)
            
        raw_translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Post-process: Replace placeholders with dictionary values
        final_translation = raw_translation
        for placeholder, value in mapping_dict.items():
            # Use regex to replace placeholder cleanly (handling spaces around placeholders if tokenizer adds them)
            # Find the placeholder token (like <1>) with or without surrounding spaces and replace it
            pattern = re.compile(rf"\s*{re.escape(placeholder)}\s*")
            final_translation = pattern.sub(f" {value} ", final_translation)
            
        # Clean up double spaces
        final_translation = re.sub(r'\s+', ' ', final_translation).strip()
        
        print(f"\n[{idx}] Input Chinese with placeholders:")
        print(f"    {zh_input}")
        print(f"    Dictionary mappings: {mapping_dict}")
        print(f"  -> Raw AI Translation (containing placeholders):")
        print(f"    {raw_translation}")
        print(f"  -> Final Enforced Translation (processed):")
        print(f"    {final_translation}")

if __name__ == "__main__":
    test_placeholder_translation()
