from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .schemas import PredictRequest, PredictResponse, EntityResult
from .model import get_ner_pipeline
from .utils import merge_entities


# -----------------------------------
# Khởi động: Load mô hình khi start
# -----------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load mô hình khi ứng dụng khởi động."""
    get_ner_pipeline()   # Pre-load
    yield
    # Dọn dẹp khi tắt ứng dụng (nếu cần)


# -----------------------------------
# Tạo FastAPI app
# -----------------------------------
app = FastAPI(
    title="NER API",
    description=(
        "API nhận dạng thực thể có tên (Named Entity Recognition) "
        "sử dụng mô hình BERT từ Hugging Face."
    ),
    version="1.0.0",
    lifespan=lifespan
)

# CORS (cho phép gọi API từ trình duyệt)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


# -----------------------------------
# Endpoint 1: GET /
# -----------------------------------
@app.get("/", summary="Giới thiệu hệ thống")
async def root():
    """Trả về thông tin mô tả về API."""
    return {
        "name": "NER API",
        "version": "1.0.0",
        "description": "Named Entity Recognition sử dụng BERT",
        "model": "sartajbhuvaji/bert-named-entity-recognition",
        "endpoints": {
            "GET /":         "Thông tin hệ thống",
            "GET /health":   "Kiểm tra trạng thái",
            "POST /predict": "Nhận dạng thực thể trong văn bản"
        }
    }


# -----------------------------------
# Endpoint 2: GET /health
# -----------------------------------
@app.get("/health", summary="Kiểm tra trạng thái hệ thống")
async def health_check():
    """Kiểm tra xem mô hình đã sẵn sàng hay chưa."""
    try:
        pipe = get_ner_pipeline()
        model_ready = pipe is not None
        return {
            "status": "healthy" if model_ready else "loading",
            "model_loaded": model_ready,
            "model_name": "sartajbhuvaji/bert-named-entity-recognition"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Mô hình chưa sẵn sàng: {str(e)}")


# -----------------------------------
# Endpoint 3: POST /predict
# -----------------------------------
@app.post(
    "/predict",
    response_model=PredictResponse,
    summary="Nhận dạng thực thể",
    response_description="Danh sách các thực thể được phát hiện trong văn bản"
)
async def predict(request: PredictRequest):
    """
    Nhận văn bản tiếng Anh đầu vào, trả về danh sách
    các thực thể được nhận dạng (người, tổ chức, địa điểm...).
    """
    # Kiểm tra đầu vào
    text = request.text.strip()
    if not text:
        raise HTTPException(
            status_code=422,
            detail="Văn bản đầu vào không được để trống."
        )

    try:
        pipe = get_ner_pipeline()
        raw_results = pipe(text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi gọi mô hình: {str(e)}"
        )

    # Gộp token và tạo danh sách EntityResult
    merged = merge_entities(raw_results)
    entities = [
        EntityResult(
            word=ent["word"],
            label=ent["label"],
            score=round(ent["score"], 4),
            start=ent["start"],
            end=ent["end"]
        )
        for ent in merged
    ]

    return PredictResponse(
        text=text,
        entities=entities,
        entity_count=len(entities)
    )
