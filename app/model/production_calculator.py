import math


def calculate_actual_production(shortage: int, yield_rate: float) -> int:
    return math.ceil(shortage / yield_rate)


def calculate_production_time(avg_production_time: float, actual_production: int) -> float:
    return avg_production_time * actual_production
