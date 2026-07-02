# HƯỚNG DẪN CẤU HÌNH TỪ ĐIỂN RIÊNG (CUSTOM DICTIONARY) & THIẾT LẬP DATA TRAIN CHI TIẾT

Hướng dẫn này giúp bạn tự tích hợp bộ **Từ điển ghép Trung - Việt riêng** của bạn vào hệ thống gán nhãn, và giải thích chi tiết cách mô hình học cách sắp xếp từ Hán Việt/Thành ngữ/Câu thơ.

---

## 1. Cách tích hợp Từ điển ghép Trung - Việt riêng của bạn

Nếu bạn đã có sẵn một file từ điển chứa các từ ghép Trung - Việt (ví dụ: `非常` -> `phi thường`, `大桥` -> `đại kiều`), bạn hãy làm theo các bước sau để tích hợp vào công cụ:

### Bước 1: Tạo file từ điển riêng
Lưu file từ điển của bạn dưới định dạng CSV vào đường dẫn:
`data/raw/custom_dict.csv`

Nội dung file có cấu trúc đơn giản như sau (phân tách bằng dấu phẩy):
```csv
zh_word,vi_word
非常,Phi Thường
人工智能,Nhân Công Trí Năng
长江大桥,Trường Giang Đại Kiều
雄伟,Hùng Vĩ
建筑,Kiến Trúc
```

### Bước 2: Chỉnh sửa bộ dịch Hán Việt (scripts/hanviet_converter.py)
Bộ dịch sẽ ưu tiên tìm trong từ điển ghép riêng của bạn trước. Nếu không có mới tự động dịch từng âm Hán Việt.
Đoạn code tích hợp trong `hanviet_converter.py` sẽ tự động load file `custom_dict.csv` nếu file này tồn tại:
```python
# Tự động nạp từ điển riêng nếu có
self.custom_map = {}
custom_csv = os.path.join(RAW_DIR, "custom_dict.csv")
if os.path.exists(custom_csv):
    with open(custom_csv, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None) # Bỏ qua header
        for row in reader:
            if len(row) >= 2:
                self.custom_map[row[0]] = row[1]
```

Khi dịch từ:
```python
def convert_word(self, word):
    # Ưu tiên từ điển ghép riêng
    if word in self.custom_map:
        return self.custom_map[word]
    # Nếu không có, tự dịch từng chữ Hán Việt
    ...
```

---

## 2. Chi tiết cấu trúc dữ liệu để AI học (Data Train Format)

Dữ liệu để nạp vào AI train phải được đóng gói dưới định dạng JSONL, mỗi dòng là một cặp câu độc lập có cấu trúc:

```json
{
  "zh_tagged": "南京市<vi: Nam Kinh Thị|ns>长江大桥<vi: Trường Giang Đại Kiều|ns>...",
  "vi": "Trường Giang Đại Kiều thành phố Nam Kinh..."
}
```

### Cách hoạt động của các Tag:
- **Từ tiếng Trung gốc:** Nằm ngay trước thẻ `<vi: ...>`.
- **Bản dịch Hán Việt ép buộc:** Nằm sau dấu `<vi: ` và trước dấu `|`.
- **Nhãn loại từ (POS Tag):** Nằm sau dấu `|` và trước dấu `>`.

---

## 3. Cách mô hình AI đọc và sắp xếp lại từ ngữ trôi chảy

Khi đưa câu vào quá trình huấn luyện:

### A. Cơ chế chú ý (Cross-Attention Mechanism)
Mô hình dịch Transformer có 2 phần chính: **Encoder (Đọc câu Trung có tag)** và **Decoder (Viết câu dịch Việt)**.
- Khi Encoder đọc câu có gắn tag `<vi: Trường Giang Đại Kiều|ns>`, nó sẽ mã hóa cụm từ này cùng với nhãn loại từ `ns` (địa danh).
- Trong quá trình Train, Decoder phải viết ra cụm từ `Trường Giang Đại Kiều` trong câu đích.
- Bộ tối ưu hóa (Optimizer) sẽ huấn luyện các "mối nối" (Attention Heads) học cách **trỏ thẳng sang vị trí tag `<vi: ...>` tương ứng**. AI sẽ nhận ra quy luật: *"Chỉ cần copy cụm chữ nằm trong tag tiếng Trung sang tiếng Việt là sẽ có bản dịch chuẩn xác."*

### B. Học cách đảo ngữ pháp (Reordering)
- Tiếng Trung viết: `非常 (Phó từ |d) + 雄伟 (Tính từ |a) + 的 + 建筑 (Danh từ |n)`.
- Nhờ có thẻ loại từ đi kèm, AI sẽ nhận được chuỗi nhãn: `|d` ➡️ `|a` ➡️ `|n`.
- Bản dịch đích tiếng Việt trôi chảy của bạn là: `kiến trúc (Danh từ) + phi thường (Phó từ) + hùng vĩ (Tính từ)`.
- AI sẽ tự động học được luật dịch chuyển nhãn: **`[|d] [|a] [|n]` dịch thành `[|n] [|d] [|a]`**. Do đó, nó sẽ tự động sắp xếp lại trật tự từ rất trơn tru.

---

## 4. Quy trình xử lý Thành ngữ (Idioms) và Thơ cổ (Poems)

Đối với các cụm thành ngữ hoặc câu thơ khó dịch, bạn nên xử lý như sau:

1. **Chuẩn bị từ điển thành ngữ/thơ cổ:** Bạn chèn các cặp dịch thành ngữ hoặc câu thơ bạn muốn giữ nguyên vào file `custom_dict.csv`.
   *Ví dụ:* `更上一层楼,Canh Thượng Nhất Tầng Lâu`
2. **Chạy tiền xử lý (Tool):** Khi chạy qua script `prepare_constrained_data.py`, công cụ sẽ dùng Jieba cắt từ.
   - Thấy cụm thành ngữ `更上一层楼`, công cụ tra trong từ điển riêng thấy nghĩa tương ứng là `Canh Thượng Nhất Tầng Lâu` và loại từ là `i` (thành ngữ).
   - Tự động đóng gói thành tag: `更上一层楼<vi: Canh Thướng Nhất Tầng Lâu|i>`.
3. **AI đọc và lưu giữ:** Khi train, AI sẽ ghi nhớ cả cụm này là một khối thống nhất (nhờ nhãn `|i`), giúp câu dịch ra giữ nguyên âm Hán Việt cổ kính của câu thơ hoặc thành ngữ đó mà không bị phá vỡ cấu trúc.
