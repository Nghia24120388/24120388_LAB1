from typing import List, Dict, Any


def merge_entities(raw_entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Gộp các token liên tiếp có cùng thực thể thành một đơn vị hoàn chỉnh.
    Ví dụ: ["Barack" B-PER] + ["Obama" I-PER] -> ["Barack Obama" PER]
    """
    if not raw_entities:
        return []

    merged = []
    current = None

    for ent in raw_entities:
        label = ent["entity"]

        # Tách prefix B- / I- để lấy nhãn gốc
        if label.startswith("B-"):
            if current:
                merged.append(current)
            current = {
                "word": ent["word"].replace("##", ""),
                "label": label[2:],  # Bỏ "B-"
                "score": ent["score"],
                "start": ent["start"],
                "end": ent["end"]
            }
        elif label.startswith("I-") and current and label[2:] == current["label"]:            # Nối tiếp thực thể hiện tại
            word = ent["word"].replace("##", "")
            # Xử lý subword token (có dấu ## thì không thêm khoảng trắng)
            if ent["word"].startswith("##"):
                current["word"] += word
            else:
                current["word"] += " " + word
            current["end"] = ent["end"]
            current["score"] = (current["score"] + ent["score"]) / 2
        else:
            if current:
                merged.append(current)
            current = None

    if current:
        merged.append(current)

    return merged
