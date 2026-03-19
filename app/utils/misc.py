from typing import Any

def _as_list(payload: Any) -> Any:
    if isinstance(payload, tuple):
        return [_as_list(item) for item in payload]
    if hasattr(payload, "tolist"):
        return payload.tolist()
    return payload
