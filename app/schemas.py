from pydantic import BaseModel, Field
from typing import List


class PredictRequest(BaseModel):
    """Cấu trúc dữ liệu đầu vào."""
    text: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Câu văn tiếng Anh cần nhận dạng thực thể",
        example="Barack Obama was born in Hawaii."
    )


class EntityResult(BaseModel):
    """Một thực thể được nhận dạng."""
    word: str = Field(..., description="Từ / cụm từ là thực thể")
    label: str = Field(..., description="Nhãn NER (ví dụ: PER, ORG, LOC)")
    score: float = Field(..., description="Độ tin cậy của mô hình (0.0 - 1.0)")
    start: int = Field(..., description="Vị trí bắt đầu trong chuỗi gốc")
    end: int = Field(..., description="Vị trí kết thúc trong chuỗi gốc")


class PredictResponse(BaseModel):
    """Kết quả trả về từ API."""
    text: str = Field(..., description="Văn bản đầu vào gốc")
    entities: List[EntityResult] = Field(..., description="Danh sách các thực thể được nhận dạng")
    entity_count: int = Field(..., description="Tổng số thực thể tìm được")
