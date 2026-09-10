from app.finance import (
    calculate_compound_interest,
    calculate_simple_interest,
    calculate_sip,
)


def test_calculate_simple_interest():
    interest, amount = calculate_simple_interest(1000, 10, 2)
    assert interest == 200.0
    assert amount == 1200.0


def test_calculate_compound_interest():
    interest, amount = calculate_compound_interest(1000, 10, 2, 4)
    assert round(interest, 2) == 215.51
    assert round(amount, 2) == 1215.51


def test_calculate_sip():
    total_invested, estimated_returns, final_value = calculate_sip(1000, 12, 1)
    assert total_invested == 12000.0
    assert round(estimated_returns, 2) == 682.42
    assert round(final_value, 2) == 12682.42
