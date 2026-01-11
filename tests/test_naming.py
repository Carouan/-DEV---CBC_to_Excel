import pytest

pandas = pytest.importorskip("pandas")

from core.naming import build_period_string


def test_build_period_string_same_month() -> None:
    df = pandas.DataFrame(
        {"Date": pandas.to_datetime(["2024-03-02", "2024-03-27"], format="%Y-%m-%d")}
    )

    period = build_period_string(df)

    assert period == "[2-27(03.24)]"


def test_build_period_string_same_year_different_month() -> None:
    df = pandas.DataFrame(
        {"Date": pandas.to_datetime(["2024-03-02", "2024-05-27"], format="%Y-%m-%d")}
    )

    period = build_period_string(df)

    assert period == "[2.03-27.05(2024)]"
