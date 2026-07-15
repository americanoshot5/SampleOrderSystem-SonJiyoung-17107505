from app.model.production_calculator import (
    calculate_actual_production,
    calculate_production_time,
)


def test_calculate_actual_production_rounds_up():
    assert calculate_actual_production(170, 0.92) == 185


def test_calculate_actual_production_exact_division():
    assert calculate_actual_production(46, 0.92) == 50


def test_calculate_production_time_multiplies_avg_time_by_actual_production():
    assert calculate_production_time(0.8, 185) == 148.0
