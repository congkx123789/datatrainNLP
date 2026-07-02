import json
import os
import random

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
PROCESSED_DIR = os.path.join(DATA_DIR, 'processed')
os.makedirs(PROCESSED_DIR, exist_ok=True)

def main():
    dataset = []

    # 1. Template: A và B là bạn tốt (20 sentences)
    # Source: A<1|nr>和B<2|nr>是好朋友。 -> Target: <1> và <2> là bạn tốt.
    for i in range(20):
        zh_tagged = "张三<1|nr>和李四<2|nr>是好朋友。"
        vi = "<1> và <2> là bạn tốt."
        dataset.append({"zh_raw": "张三和李四是好朋友。", "zh_tagged": zh_tagged, "vi": vi, "has_hint": True})

    # 2. Template: A đi đến B (20 sentences)
    # Source: A<1|nr>去B<2|ns>。 -> Target: <1> đi đến <2>.
    for i in range(20):
        zh_tagged = "张三<1|nr>去南京市<2|ns>。"
        vi = "<1> đi đến <2>."
        dataset.append({"zh_raw": "张三去南京市。", "zh_tagged": zh_tagged, "vi": vi, "has_hint": True})

    # 3. Template: A là kiến trúc B (20 sentences)
    # Source: 南京市<1|ns>长江大桥<2|ns>是非常<3|d>雄伟<4|a>的建筑<5|n>。 -> Target: <2> thành phố <1> là <5> <3> <4>.
    for i in range(20):
        zh_tagged = "南京市<1|ns>长江大桥<2|ns>是非常<3|d>雄伟<4|a>的建筑<5|n>。"
        vi = "<2> thành phố <1> là <5> <3> <4>."
        dataset.append({"zh_raw": "南京市长江大桥是非常雄伟的建筑。", "zh_tagged": zh_tagged, "vi": vi, "has_hint": True})

    # 4. Template: Cô ấy học ở A để nghiên cứu B (20 sentences)
    # Source: 她在北京大学<1|nt>学习人工智能<2|n>。 -> Target: Cô ấy học ở <1> để nghiên cứu <2>.
    for i in range(20):
        zh_tagged = "她在北京大学<1|nt>学习人工智能<2|n>。"
        vi = "Cô ấy học ở <1> để nghiên cứu <2>."
        dataset.append({"zh_raw": "她在北京大学学习人工智能。", "zh_tagged": zh_tagged, "vi": vi, "has_hint": True})

    # 5. Template: Anh ấy là A (20 sentences)
    # Source: 他是好朋友<1|n>。 -> Target: Anh ấy là <1>.
    for i in range(20):
        zh_tagged = "他是好朋友<1|n>。"
        vi = "Anh ấy là <1>."
        dataset.append({"zh_raw": "他是好朋友。", "zh_tagged": zh_tagged, "vi": vi, "has_hint": True})

    out_path = os.path.join(PROCESSED_DIR, "train_constrained.jsonl")
    with open(out_path, 'w', encoding='utf-8') as f:
        for item in dataset:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
            
    print(f"Generated {len(dataset)} hybrid POS-index placeholder sentences at {out_path}")

if __name__ == "__main__":
    main()
