# HƯỚNG DẪN SETUP MÁY MỚI & PHỤC HỒI DỮ LIỆU CHUẨN

Tài liệu này hướng dẫn bạn cách thiết lập lại dự án từ đầu trên một máy tính khác và khôi phục toàn bộ cấu trúc dữ liệu thô (raw data) chuẩn để hệ thống chạy ổn định.

---

## 1. Thiết lập môi trường trên máy tính mới

### Bước 1: Tải mã nguồn về máy
Mở Terminal (hoặc Command Prompt / PowerShell) và chạy lệnh:
```bash
git clone https://github.com/congkx123789/datatrainNLP.git
cd datatrainNLP
```

### Bước 2: Tạo môi trường ảo (Virtual Environment)
Để tránh xung đột thư viện:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### Bước 3: Cài đặt các thư viện cần thiết
Chạy lệnh cài đặt toàn bộ thư viện từ file `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

## 2. Phục hồi cấu trúc thư mục & dữ liệu thô (Raw Data)

Do các file dữ liệu thô (raw) và mô hình rất nặng nên không được đẩy lên GitHub. Bạn cần chạy các script phục hồi tự động để sinh lại chúng.

### Cấu trúc thư mục dữ liệu chuẩn cần khôi phục:
```text
datatrainNLP/
├── data/
│   ├── raw/
│   │   ├── THUOCL/                   <-- Từ điển Đại học Thanh Hoa (Tự động tải)
│   │   ├── hanlp_dict.txt            <-- Từ điển HanLP (Tự động tải)
│   │   ├── jieba_dict.txt            <-- Từ điển Jieba (Tự động tải)
│   │   ├── hanviet.csv               <-- Từ điển Hán Việt (Tự động tải)
│   │   ├── zh_vi_tatoeba.jsonl       <-- File song ngữ mẫu (Tự động tạo)
│   │   └── zh_vi_opensubtitles.jsonl <-- File dữ liệu song ngữ lớn (Nếu có)
│   └── processed/
│       ├── jieba_filtered_4plus.txt  <-- Từ điển Jieba lọc từ >= 4 ký tự (Tự động tạo)
│       ├── hanlp_filtered_4plus.txt  <-- Từ điển HanLP lọc từ >= 4 ký tự (Tự động tạo)
│       └── train_constrained.jsonl   <-- Dữ liệu train điền chỗ trống cuối cùng (Tự động tạo)
```

---

## 3. Các lệnh phục hồi dữ liệu tự động (Chạy theo thứ tự)

Chạy lần lượt các lệnh sau trong thư mục dự án để phục hồi 100% dữ liệu thô và dữ liệu đã tiền xử lý:

### Lệnh 1: Tải và giải nén các từ điển phân tách từ (Jieba, HanLP, THUOCL)
Lệnh này sẽ tự động tải các bộ từ điển gốc Trung Quốc từ internet và lọc lấy các từ ghép dài >= 4 chữ Hán:
```bash
python scripts/filter_lexicons.py
```

### Lệnh 2: Tải dữ liệu từ điển Hán Việt (hanviet.csv)
Lệnh này tải bảng ánh xạ chữ Hán sang âm Hán Việt chuẩn:
```bash
python scripts/download_hanviet_csv.py
```

### Lệnh 3: Tạo dữ liệu song ngữ Trung - Việt mẫu (zh_vi_tatoeba.jsonl)
Tạo file dữ liệu song ngữ chuẩn có chứa các câu thơ cổ, thành ngữ và tên riêng mẫu:
```bash
python scripts/prepare_synthetic_data.py
```

### Lệnh 4: Chạy tiền xử lý chèn thẻ gợi ý (Dữ liệu train cuối cùng)
Lệnh này đọc dữ liệu song ngữ thô, chạy Jieba phân tích cú pháp, tra từ điển Hán Việt và đóng gói ra file `train_constrained.jsonl` chứa các tag cưỡng bức dạng `<vi: ...>`:
```bash
python scripts/prepare_constrained_data.py
```

---

## 4. Kiểm tra xem hệ thống đã hoạt động chuẩn chưa
Sau khi chạy xong 4 lệnh trên, bạn có thể chạy thử lệnh kiểm tra tốc độ dịch thuật để đảm bảo môi trường đã cài đặt hoàn hảo:
```bash
python scripts/optimize_and_benchmark.py
```
Nếu màn hình xuất ra bảng đo tốc độ dịch chi tiết với chỉ số **~240 tokens/s** (cho model 74M) và **~980 tokens/s** (cho model Tiny 17M) thì hệ thống của bạn trên máy mới đã được setup thành công 100%!
