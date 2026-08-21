import pytest

from app.domain.stats import calculate_stats


def test_calculate_stats_returns_min_max_avg() -> None:
    result = calculate_stats([10.0, 20.0, 30.0])
    assert result.minimum == 10.0
    assert result.maximum == 30.0
    assert result.average == 20.0


def test_calculate_stats_single_value() -> None:
    result = calculate_stats([15.0])
    assert result.minimum == 15.0
    assert result.maximum == 15.0
    assert result.average == 15.0


def test_calculate_stats_empty_list_raises_value_error() -> None:
    with pytest.raises(ValueError, match="al menos una lectura"):
        calculate_stats([])