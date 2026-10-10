"""Tests unitaires pour la conformité et le calcul du taux d'endettement."""

from utils import calculate_debt_ratio, estimate_borrowing_capacity


def test_debt_ratio_calculation():
    ratio = calculate_debt_ratio(monthly_income=2000.0, monthly_charges=600.0)
    assert ratio == 30.0


def test_borrowing_capacity_positive():
    capacity = estimate_borrowing_capacity(monthly_income=3000.0, existing_loans=200.0)
    assert capacity["max_monthly_payment"] > 0
    assert capacity["total_capacity"] > 0
