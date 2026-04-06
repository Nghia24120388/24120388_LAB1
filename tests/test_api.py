import requests
import json

BASE_URL = "http://localhost:8000"


def print_separator(title: str):
    print("\n" + "=" * 55)
    print(f"  {title}")
    print("=" * 55)


# ----------------------------------------
# Test 1: GET /
# ----------------------------------------
print_separator("Test 1: GET /")
resp = requests.get(f"{BASE_URL}/")
print(f"Status: {resp.status_code}")
print(json.dumps(resp.json(), indent=2, ensure_ascii=False))

# ----------------------------------------
# Test 2: GET /health
# ----------------------------------------
print_separator("Test 2: GET /health")
resp = requests.get(f"{BASE_URL}/health")
print(f"Status: {resp.status_code}")
print(json.dumps(resp.json(), indent=2, ensure_ascii=False))

# ----------------------------------------
# Test 3: POST /predict -- Đầu vào hợp lệ 1
# ----------------------------------------
print_separator("Test 3: POST /predict - Hợp lệ (người + địa điểm)")
payload = {"text": "Barack Obama was born in Hawaii and studied at Harvard."}
resp = requests.post(f"{BASE_URL}/predict", json=payload)
print(f"Status: {resp.status_code}")
data = resp.json()
print(f"Văn bản: {data['text']}")
print(f"Số thực thể: {data['entity_count']}")
for ent in data["entities"]:
    print(f"  [{ent['label']}] {ent['word']!r:<25} (score={ent['score']:.4f})")

# ----------------------------------------
# Test 4: POST /predict -- Đầu vào hợp lệ 2
# ----------------------------------------
print_separator("Test 4: POST /predict - Hợp lệ (tổ chức + địa điểm)")
payload = {"text": "Google was founded in California by Larry Page and Sergey Brin."}
resp = requests.post(f"{BASE_URL}/predict", json=payload)
print(f"Status: {resp.status_code}")
data = resp.json()
print(f"Văn bản: {data['text']}")
print(f"Số thực thể: {data['entity_count']}")
for ent in data["entities"]:
    print(f"  [{ent['label']}] {ent['word']!r:<25} (score={ent['score']:.4f})")

# ----------------------------------------
# Test 5: POST /predict -- Đầu vào không hợp lệ
# ----------------------------------------
print_separator("Test 5: POST /predict - Đầu vào rỗng (lỗi 422)")
payload = {"text": "   "}
resp = requests.post(f"{BASE_URL}/predict", json=payload)
print(f"Status: {resp.status_code}")
print(json.dumps(resp.json(), indent=2, ensure_ascii=False))

# ----------------------------------------
# Test 6: POST /predict -- Thiếu trường 'text'
# ----------------------------------------
print_separator("Test 6: POST /predict - Thiếu trường text (lỗi 422)")
payload = {}
resp = requests.post(f"{BASE_URL}/predict", json=payload)
print(f"Status: {resp.status_code}")
print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
