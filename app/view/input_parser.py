def parse_int(text: str) -> int | None:
    try:
        return int(text)
    except ValueError:
        return None


def parse_float(text: str) -> float | None:
    try:
        return float(text)
    except ValueError:
        return None
