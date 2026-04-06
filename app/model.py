from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    pipeline
)
import torch

_ner_pipeline = None  # Biến global để lưu pipeline


def get_ner_pipeline():
    """
    Trả về NER pipeline. Nếu chưa khởi tạo thì load mô hình trước.
    Sử dụng Singleton Pattern để tránh load nhiều lần.
    """
    global _ner_pipeline

    if _ner_pipeline is None:
        model_name = "sartajbhuvaji/bert-named-entity-recognition"
        print(f"[INFO] Đang tải mô hình: {model_name}")

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForTokenClassification.from_pretrained(model_name)

        device = 0 if torch.cuda.is_available() else -1  # GPU nếu có
        _ner_pipeline = pipeline(
            "token-classification",
            model=model,
            tokenizer=tokenizer,
            device=device
        )
        print("[INFO] Mô hình đã sẵn sàng!")

    return _ner_pipeline
