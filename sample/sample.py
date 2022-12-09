__types = {
    "a": int,
    "b": int
}

def run(payload: dict) -> dict:
    a = payload.get("a")
    b = payload.get("b")
    return [a+b, None]