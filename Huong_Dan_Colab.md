# HƯỚNG DẪN HUẤN LUYỆN (TRAINING) MÔ HÌNH DỊCH THUẬT TRÊN GOOGLE COLAB

Vì máy cá nhân không có card đồ họa GPU NVIDIA mạnh hỗ trợ CUDA, bạn nên tải toàn bộ thư mục dự án này lên Google Colab để chạy huấn luyện mô hình hoàn toàn miễn phí.

Dưới đây là các bước thực hiện trên Google Colab:

---

### BƯỚC 1: Chuẩn bị Thư mục Dự án
1. Nén toàn bộ thư mục `tạo dữ liệu Train dịch` của bạn lại thành file `.zip` (ví dụ đặt tên là `train_project.zip`).
2. Tải file `train_project.zip` này lên tài khoản **Google Drive** của bạn.

---

### BƯỚC 2: Khởi tạo Google Colab
1. Truy cập [Google Colab](https://colab.research.google.com/).
2. Chọn **New notebook (Sổ tay mới)**.
3. Ở góc trên bên phải, bấm vào mũi tên cạnh nút **Connect (Kết nối)** ➡️ Chọn **Change runtime type (Thay đổi loại môi trường chạy)**.
4. Tại mục **Hardware accelerator (Bộ tăng tốc phần cứng)**, chọn **GPU T4** (miễn phí) ➡️ Bấm **Save (Lưu)**.

---

### BƯỚC 3: Coppy và Chạy các Cell Code sau trên Colab

#### Cell 1: Kết nối Google Drive và giải nén dự án
```python
from google.colab import drive
import os

# 1. Mount Google Drive
drive.mount('/content/drive')

# 2. Định nghĩa đường dẫn chứa file zip của bạn trên Drive
# Giả sử bạn để file zip ngay ngoài thư mục gốc của Drive
zip_path = '/content/drive/MyDrive/train_project.zip'
project_dir = '/content/translation_project'

# 3. Giải nén vào bộ nhớ đệm của Colab
if os.path.exists(zip_path):
    !unzip -q {zip_path} -d {project_dir}
    print("Giải nén thành công dự án vào Colab!")
else:
    print(f"Không tìm thấy file zip tại {zip_path}. Hãy kiểm tra lại đường dẫn trên Drive.")
```

#### Cell 2: Cài đặt các thư viện cần thiết cho huấn luyện GPU
```python
# Di chuyển vào thư mục dự án vừa giải nén
%cd /content/translation_project/tạo dữ liệu Train dịch/

# Cài đặt thư viện xử lý NLP và huấn luyện GPU tốc độ cao
!pip install -q transformers datasets accelerate sentencepiece sacremoses zhconv jieba
print("Cài đặt các thư viện thành công!")
```

#### Cell 3: Chạy chuẩn bị dữ liệu (Nếu cần làm lại dữ liệu song ngữ)
```python
# Chạy lại script chuẩn bị dữ liệu tag gợi ý từ điển
!python scripts/prepare_constrained_data.py
```

#### Cell 4: Thực hiện Huấn luyện (Fine-tuning)
```python
# Chạy script huấn luyện mô hình bằng GPU
!python scripts/train_tiny.py
```
*(Quá trình train sẽ tự động lưu checkpoints và file model hoàn chỉnh vào thư mục `models/constrained_mt_model` trên Colab).*

#### Cell 5: Test thử bản dịch từ mô hình vừa Train
Sau khi train xong, chạy đoạn code sau để test khả năng dịch điền vào chỗ trống của mô hình mới:
```python
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_path = "models/constrained_mt_model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path).to("cuda")

# Thử thách câu dịch có chứa tag gợi ý Vũ Công
test_text = "这是武功<vi: Vũ Công>的狗。"

inputs = tokenizer(test_text, return_tensors="pt").to("cuda")
outputs = model.generate(**inputs)
translated = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(f"Câu gốc có tag: {test_text}")
print(f"Bản dịch AI:    {translated}")
```

---

### BƯỚC 4: Tải mô hình đã train về máy cá nhân
Chạy cell này để nén và tải mô hình đã train xong về máy:
```python
# Nén thư mục model
!zip -r /content/my_trained_model.zip models/constrained_mt_model/

# Download file zip về máy cá nhân
from google.colab import files
files.download('/content/my_trained_model.zip')
```
Sau khi tải về máy cá nhân, bạn có thể giải nén và dùng script **CTranslate2** để tối ưu hóa và chạy dịch offline siêu tốc như chúng ta vừa thử nghiệm ở các bước trước!
