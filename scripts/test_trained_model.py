import os
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Path to the fine-tuned model
MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'constrained_mt_model'))

def test_translation(text):
    if not os.path.exists(MODEL_DIR):
        print(f"Error: Model directory not found at {MODEL_DIR}")
        return
        
    print(f"Loading fine-tuned model from {MODEL_DIR}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_DIR)
    
    # Put model in evaluation mode
    model.eval()
    
    # Tokenize input
    inputs = tokenizer(text, return_tensors="pt")
    
    print(f"\nSource Chinese with tags:\n  {text}")
    
    # Generate translation
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=128, num_beams=4, early_stopping=True)
        
    translated = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"\nAI Translation (Hán Việt style):\n  {translated}")

if __name__ == "__main__":
    # Test sample with multiple tags
    test_sentence = "南京市<vi: Nam Kinh Thị|ns>长江大桥<vi: Trường Giang Đại Kiều|ns>是非常<vi: Phi Thường|d>雄伟<vi: Hùng Vĩ|a>的建筑<vi: Kiến Trúc|n>。"
    test_translation(test_sentence)
