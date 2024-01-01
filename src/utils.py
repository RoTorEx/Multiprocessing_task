import json
import time


def get_metrics(messages: list[dict], count_type: str) -> dict:
    metrics = {
        "timestamp": int(time.time()),
        "count_type": count_type,
        "A1_sum": messages[0]["A1"],
        "A2_max": messages[0]["A2"],
        "A3_min": messages[0]["A3"],
    }
    for message in messages[1:]:
        metrics["A1_sum"] += message["A1"]
        if message["A2"] > metrics["A2_max"]:
            metrics["A2_max"] = message["A2"]
        if message["A3"] < metrics["A3_min"]:
            metrics["A3_min"] = message["A3"]
    return metrics


def write_metrics(metrics: dict) -> None:
    with open("metrics.txt", "a", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False)
        f.write("\n")
