# Báo Cáo Chi Tiết Cấu Trúc Và Trạng Thái Dữ Liệu Hiện Tại (DATA_SUMMARY.md)

Tài liệu này cung cấp cái nhìn chi tiết nhất về cấu trúc thư mục dữ liệu, kích thước tệp, số lượng dòng (cặp câu song ngữ), và cơ chế gán nhãn ràng buộc dữ liệu dịch thuật Trung - Việt hiện tại trong dự án.

---

## 1. Sơ Đồ Cấu Trúc Thư Mục Dữ Liệu (`data/`)

Dữ liệu của dự án được tổ chức khoa học thành 3 thư mục con: `raw` (dữ liệu thô tải từ HF/Github), `processed` (dữ liệu đã qua lọc từ điển và gán nhãn gợi ý Hán Việt), và `embeddings` (mã nguồn client nhúng từ Tencent).

```
datatrainNLP/
└── data/
    ├── raw/                            # Dữ liệu thô song ngữ & từ điển gốc
    │   ├── hanviet.csv                 # Từ điển ánh xạ từ đơn sang Hán Việt
    │   ├── jieba_dict.txt              # Từ điển gốc của bộ tách từ Jieba
    │   ├── hanlp_dict.txt              # Từ điển gốc của bộ tách từ HanLP
    │   ├── THUOCL/                     # Kho từ vựng chuyên ngành Đại học Thanh Hoa
    │   │   └── data/
    │   │       ├── THUOCL_IT.txt       # Từ vựng CNTT
    │   │       ├── THUOCL_medical.txt  # Từ vựng Y học
    │   │       └── ... (11 files .txt)
    │   ├── tatoeba.jsonl               # Song ngữ Anh - Trung (Tatoeba)
    │   ├── opensubtitles.jsonl         # Song ngữ Anh - Trung (OpenSubtitles)
    │   ├── wmt19.jsonl                 # Song ngữ Anh - Trung (WMT19)
    │   ├── zh_vi_tatoeba.jsonl         # Song ngữ Trung - Việt (Tatoeba gốc)
    │   └── zh_vi_opensubtitles.jsonl   # Song ngữ Trung - Việt (Từ nlp_data_zh_vi)
    │
    ├── processed/                      # Dữ liệu đã qua xử lý & lọc
    │   ├── jieba_filtered_4plus.txt    # Từ ghép Jieba >= 4 ký tự
    │   ├── hanlp_filtered_4plus.txt    # Từ ghép HanLP >= 4 ký tự
    │   ├── thuocl_filtered_4plus.txt   # Từ ghép THUOCL >= 4 ký tự
    │   └── train_constrained.jsonl     # Dataset huấn luyện Trung - Việt cuối cùng
    │
    └── embeddings/                     # Bộ nhúng từ (Word Embeddings)
        └── Conan-embedding-v2/         # Tencent AI Lab Conan-embedding-v2 client
```

---

## 2. Thống Kê Chi Tiết Các Bộ Dữ Liệu

Dưới đây là bảng thống kê chi tiết dung lượng trên đĩa cứng và số lượng cặp câu song ngữ (hoặc số lượng từ chuyên ngành) thực tế được khôi phục thành công:

| Tên Bộ Dữ Liệu | Đường Dẫn Tệp | Cặp Ngôn Ngữ | Dung Lượng | Số Dòng (Cặp Câu / Từ) | Mô Tả & Nguồn Gốc |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **WMT19** | `data/raw/wmt19.jsonl` | `en-zh` | **6.6 GB** | **25,984,574** | Dữ liệu hàn lâm (tin tức, chính phủ), câu văn dài, chuẩn ngữ pháp. |
| **OpenSubtitles** | `data/raw/opensubtitles.jsonl` | `en-zh` | **2.6 GB** | **11,203,286** | Phụ đề phim ảnh, mang tính khẩu ngữ và giao tiếp đời thường. |
| **Tatoeba (En-Zh)** | `data/raw/tatoeba.jsonl` | `en-zh` | **5.3 MB** | **53,463** | Các câu đàm thoại ngắn, cơ bản, cấu trúc chuẩn. |
| **OpenSubtitles (Zh-Vi)** | `data/raw/zh_vi_opensubtitles.jsonl` | `zh-vi` | **3.8 MB** | **18,000** | Dữ liệu huấn luyện song ngữ Trung - Việt gốc (từ `nlp_data_zh_vi`). |
| **Tatoeba (Zh-Vi)** | `data/raw/zh_vi_tatoeba.jsonl` | `zh-vi` | **48 KB** | **439** | Bộ câu đàm thoại song ngữ Trung - Việt chuẩn từ Tatoeba_mt. |
| **Từ điển Hán Việt** | `data/raw/hanviet.csv` | `zh-vi` | **191 KB** | **-** | Ánh xạ âm Hán Việt từ ký tự Trung sang tiếng Việt. |
| **THUOCL** | `data/raw/THUOCL/data/` | `zh` | **308 KB** | **98,621 (từ ghép)**| Kho từ điển chuyên ngành Đại học Thanh Hoa (11 lĩnh vực). |
| **Dataset Constrained** | `data/processed/train_constrained.jsonl` | `zh-vi` | **4.9 MB** | **18,000** | Dữ liệu huấn luyện Trung - Việt tích hợp gợi ý Hán Việt copy. |

---

## 3. Kho Từ Vựng Chuyên Ngành THUOCL (Đại học Thanh Hoa)

Bộ từ điển THUOCL được phân tách thành 11 tệp lĩnh vực chuyên biệt. Kịch bản xử lý đã quét qua toàn bộ 11 file này, lọc ra các thuật ngữ từ ghép có độ dài từ **4 chữ Hán trở lên** (length >= 4) và loại bỏ trùng lặp để lưu vào `data/processed/thuocl_filtered_4plus.txt`:

* **Tổng số từ chuyên ngành trích xuất được**: **98,621** từ ghép độc bản.
* **Các chuyên ngành bao gồm**:
  1. CNTT (`THUOCL_IT.txt`)
  2. Y học (`THUOCL_medical.txt`)
  3. Tài chính (`THUOCL_caijing.txt`)
  4. Địa danh (`THUOCL_diming.txt`)
  5. Món ăn (`THUOCL_food.txt`)
  6. Thành ngữ (`THUOCL_chengyu.txt`)
  7. Lịch sử nhân vật (`THUOCL_lishimingren.txt`)
  8. Thơ ca (`THUOCL_poem.txt`)
  9. Xe cộ (`THUOCL_car.txt`)
  10. Luật pháp (`THUOCL_law.txt`)
  11. Động vật (`THUOCL_animal.txt`)

* **Mẫu định dạng từ điển gốc**:
  ```text
  文件备份	1245
  虚拟地址	890
  C++编程	3450
  ```

---

## 4. Quy Trình Tạo Dữ Liệu Huấn Luyện Ràng Buộc Hán Việt (`train_constrained.jsonl`)

Tệp `train_constrained.jsonl` là nhân tố cốt lõi giúp mô hình dịch học cách **sao chép nguyên trạng** hoặc **tham chiếu gợi ý** các danh từ riêng, thuật ngữ khó trong quá trình huấn luyện dịch Trung - Việt.

### 4.1 Cơ Chế Hoạt Động (Cấu trúc Hinting)
1. **Tổng hợp từ ghép**: Hệ thống tải **186,145** từ ghép có độ dài $\ge 4$ ký tự từ 3 nguồn: Jieba, HanLP, và THUOCL.
2. **Phân tích cú pháp**: Câu tiếng Trung gốc (`zh_raw`) được phân tích cú pháp/tách từ bằng `jieba` và mô hình gắn nhãn loại từ.
3. **Ánh xạ Hán Việt**: Với mỗi từ ghép hoặc tên riêng (`flag == 'nr'`, tên lịch sử, hoặc từ trong THUOCL) tìm thấy, hệ thống chuyển đổi từ đó sang âm Hán Việt tương ứng (ví dụ: `胡萝卜` -> `Hồ La Bốc`).
4. **Kiểm tra trùng khớp**: Nếu âm Hán Việt đó (hoặc các âm thành phần có độ dài > 2 ký tự) xuất hiện trong câu tiếng Việt mục tiêu (`vi`), nhãn gợi ý `<vi: ...>` sẽ được chèn trực tiếp sau từ tiếng Trung đó.
5. **Định dạng đầu ra**:
   * `zh_raw`: Câu tiếng Trung nguyên bản.
   * `zh_tagged`: Câu tiếng Trung đã được chèn gợi ý constraint phục vụ làm Input cho mô hình Seq2Seq.
   * `vi`: Câu tiếng Việt đích phục vụ làm Target.
   * `has_hint`: Gắn nhãn `True` nếu câu có chứa gợi ý gợi mở copy, ngược lại là `False`.

### 4.2 Mẫu Dữ Liệu Thực Tế Trong Tệp `train_constrained.jsonl`
Dưới đây là một số ví dụ thực tế đã xử lý thành công:

* **Ví dụ 1 (Từ chuyên ngành thực phẩm/cây trồng)**:
  * **Trung gốc**: `看情况给土壤添加有机肥料.`
  * **Trung chèn nhãn**: `看情况给土壤添加有机肥料<vi: Hữu Cơ Phì Liệu>.`
  * **Việt đích**: `bón phân hữu cơ nếu cần.`
  * **Nhận xét**: Từ ghép `有机肥料` được chuyển thành Hán Việt `Hữu Cơ Phì Liệu` và được chèn gợi ý do trùng với cụm "phân hữu cơ" trong câu dịch tiếng Việt.

* **Ví dụ 2 (Thuật ngữ Y học)**:
  * **Trung gốc**: `实际上,今年二月有一项非常有趣的调查,他们发现能够分离出沙门氏菌.`
  * **Trung chèn nhãn**: `实际上,今年二月有一项非常有趣的调查,他们发现能够分离出沙门氏菌<vi: Sa Môn Thị Khuẩn>.`
  * **Việt đích**: `và thực ra vào tháng hai vừa qua, đã có một nghiên cứu rất thú vị cho thấy họ có thể phân lập salmonella.`

* **Ví dụ 3 (Tên tổ chức chuyên ngành)**:
  * **Trung gốc**: `作为一名在韩国疾控中心, 中国疾控中心和其他国家疾病控制政府相关机构工作的学生.`
  * **Trung chèn nhãn**: `作为一名在韩国疾控中心<vi: Tật Khống Trung Tâm>, 中国疾控中心<vi: Tật Khống Trung Tâm>和其他国家疾病控制政府相关机构工作的学生.`
  * **Việt đích**: `là một sinh viên làm việc cho cdc hàn quốc, cdc trung quốc và các tổ chức chính phủ liên quan đến kiểm soát dịch bệnh khác.`

---

## 5. Hướng Dẫn Sử Dụng Và Huấn Luyện

### 5.1 Khôi phục lại toàn bộ dữ liệu từ đầu
Nếu muốn chạy lại toàn bộ quy trình tải, lọc và xử lý dữ liệu:
```bash
# Bước 1: Khôi phục từ điển Hán Việt & các từ điển phụ trợ
python3 scripts/filter_lexicons.py

# Bước 2: Tải dữ liệu thô song ngữ Trung - Việt
python3 scripts/download_zh_vi_data.py

# Bước 3: Gán nhãn dữ liệu ràng buộc Hán Việt
python3 scripts/prepare_constrained_data.py
```

### 5.2 Huấn luyện thử nghiệm nhanh trên GPU (GeForce RTX 5060 Ti)
Để chạy thử luồng huấn luyện fine-tuning mô hình dịch thuật ràng buộc trên GPU local:
```bash
python3 scripts/train_tiny.py
```
*Script này sẽ tự động thêm các token đặc biệt `<vi:` và `>` vào tokenizer của mô hình `Helsinki-NLP/opus-mt-zh-vi`, điều chỉnh embedding layer và chạy huấn luyện 5 epochs.*
