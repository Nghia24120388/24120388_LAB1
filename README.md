# NER API — Named Entity Recognition

## Thông tin sinh viên

- **Họ tên:** Lê Đại Nghĩa
- **MSSV:** 24120388
- **Lớp:** 24CTT1

---

## Mô hình

- **Tên:** `sartajbhuvaji/bert-named-entity-recognition`
- **Kiến trúc:** BERT fine-tuned cho Token Classification (NER)
- **Link:** https://huggingface.co/sartajbhuvaji/bert-named-entity-recognition
- **Ngôn ngữ:** Tiếng Anh

---

## Mô tả hệ thống

API nhận văn bản tiếng Anh và trả về danh sách các thực thể được nhận dạng (người, tổ chức, địa điểm, ...) sử dụng mô hình BERT từ Hugging Face, được triển khai bằng FastAPI.

**Các endpoint:**

| Endpoint   | Method | Mô tả                            |
| ---------- | ------ | -------------------------------- |
| `/`        | GET    | Thông tin hệ thống               |
| `/health`  | GET    | Kiểm tra trạng thái mô hình      |
| `/predict` | POST   | Nhận dạng thực thể trong văn bản |

---

## Cài đặt

```bash
# Tạo môi trường ảo
python -m venv venv

# Kích hoạt (Linux / macOS)
source venv/bin/activate

# Kích hoạt (Windows)
source venv/Scripts/activate

# Cài đặt thư viện
pip install -r requirements.txt
```

---

## Chạy chương trình

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Khi thấy thông báo `Uvicorn running on http://0.0.0.0:8000`, server đã sẵn sàng.

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## Ví dụ gọi API

### Bằng `curl`

```bash
curl -X POST http://localhost:8000/predict \
     -H "Content-Type: application/json" \
     -d '{"text": "Elon Musk founded SpaceX in California."}'
```

### Bằng Python

```python
import requests

resp = requests.post(
    "http://localhost:8000/predict",
    json={"text": "Barack Obama was born in Hawaii and studied at Harvard."}
)
print(resp.json())
```

### Kết quả mẫu

```json
{
  "text": "Barack Obama was born in Hawaii and studied at Harvard.",
  "entities": [
    {
      "word": "Barack Obama",
      "label": "PER",
      "score": 0.998,
      "start": 0,
      "end": 12
    },
    {
      "word": "Hawaii",
      "label": "LOC",
      "score": 0.9965,
      "start": 25,
      "end": 31
    },
    {
      "word": "Harvard",
      "label": "ORG",
      "score": 0.9943,
      "start": 46,
      "end": 53
    }
  ],
  "entity_count": 3
}
```

---

## Kiểm thử

```bash
python tests/test_api.py
```

---

## Cấu trúc dự án

```
ner-api/
├── app/
│   ├── __init__.py
│   ├── main.py       # FastAPI application chính
│   ├── model.py      # Load và quản lý mô hình
│   ├── schemas.py    # Pydantic models (request/response)
│   └── utils.py      # Hàm tiện ích xử lý kết quả NER
├── tests/
│   └── test_api.py   # Kiểm thử API bằng thư viện requests
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Video demo

https://github.com/user-attachments/assets/dc504d73-718d-4992-b617-c76d2742d094
