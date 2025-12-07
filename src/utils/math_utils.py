from typing import Union

Number = Union[int, float]


def clamp(value: Number, min_value: Number, max_value: Number) -> float:
    """Değeri min-max aralığına sıkıştır."""
    v = float(value)
    if v < min_value:
        return float(min_value)
    if v > max_value:
        return float(max_value)
    return v


def safe_div(numerator: Number, denominator: Number, default: float = 0.0) -> float:
    """Sıfıra bölme durumunu engelle."""
    if denominator in (0, 0.0):
        return float(default)
    return float(numerator) / float(denominator)
