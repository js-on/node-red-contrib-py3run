def run(payload: dict) -> dict:
    a = payload.get("a")
    b = payload.get("b")
    if not a or not b:
        return [None, "Either a or b is missing"]
    elif type(a) not in [float, int] or type(b) not in [float, int]:
        return [None, "Either a or b is not numeric"]
    
    return [a+b, None]