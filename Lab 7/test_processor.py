import math
import re

import pytest
from hypothesis import given, strategies as st

from processor import (
    calculate_depreciation_factor,
    lookup_condition_multiplier,
    verify_isbn10_format,
)


CONDITION_MULTIPLIERS = {
    "MINT": 1.25,
    "LIKE_NEW": 1.00,
    "VERY_GOOD": 0.80,
    "GOOD": 0.60,
    "POOR": 0.30,
}


def _is_isbn10_format(value):
    if not isinstance(value, str):
        return False
    cleaned = value.replace("-", "").strip()
    return re.fullmatch(r"[0-9]{9}[0-9Xx]", cleaned) is not None


def _is_valid_age_lifespan(value):
    if not isinstance(value, str):
        return False
    parts = value.split("/")
    if len(parts) != 2:
        return False
    try:
        age, lifespan = (float(part) for part in parts)
    except ValueError:
        return False
    return (
        math.isfinite(age)
        and math.isfinite(lifespan)
        and age >= 0
        and lifespan > 0
    )


@st.composite
def isbn10_values(draw):
    digits = draw(st.text(alphabet="0123456789", min_size=9, max_size=9))
    check_character = draw(st.sampled_from("0123456789X"))
    return f"{digits[0]}-{digits[1:4]}-{digits[4:9]}-{check_character}"


@given(isbn10_values())
def test_verify_isbn10_format_extracts_fields(isbn):
    cleaned = isbn.replace("-", "")
    assert verify_isbn10_format(isbn) == (
        f"Group {cleaned[1:4]}: Starts {cleaned[0]}, "
        f"Checksum {cleaned[9]}"
    )


@given(st.text(max_size=500).filter(lambda value: not _is_isbn10_format(value)))
def test_verify_isbn10_format_rejects_malformed_strings(value):
    with pytest.raises(ValueError):
        verify_isbn10_format(value)


@pytest.mark.parametrize(
    "value",
    [
        "",
        "123456789",
        "12345678901",
        "ABCDEFGHIJ",
        "12345678X0",
        "０１２３４５６７８９",
        "1" * 10000,
    ],
)
def test_verify_isbn10_format_rejects_known_malformed_strings(value):
    with pytest.raises(ValueError):
        verify_isbn10_format(value)


@given(
    st.one_of(
        st.none(),
        st.booleans(),
        st.integers(),
        st.floats(allow_nan=True),
        st.binary(),
        st.lists(st.text()),
        st.dictionaries(st.text(), st.text()),
    )
)
def test_verify_isbn10_format_rejects_non_strings(value):
    with pytest.raises(TypeError):
        verify_isbn10_format(value)


@given(
    st.integers(min_value=0, max_value=10**100),
    st.integers(min_value=1, max_value=10**100),
)
def test_calculate_depreciation_factor_is_bounded(age, lifespan):
    result = calculate_depreciation_factor(f"{age}/{lifespan}")
    expected = round(max(0.1, 1.0 - (age / lifespan)), 2)
    assert result == expected
    assert 0.1 <= result <= 1.0


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("0/1e308", 1.0),
        ("1e308/1e308", 0.1),
        ("1e308/1e-308", 0.1),
    ],
)
def test_calculate_depreciation_factor_handles_float_boundaries(value, expected):
    assert calculate_depreciation_factor(value) == expected


@given(st.text(max_size=500).filter(lambda value: not _is_valid_age_lifespan(value)))
def test_calculate_depreciation_factor_rejects_invalid_ratios(value):
    with pytest.raises(ValueError):
        calculate_depreciation_factor(value)


@pytest.mark.parametrize(
    "value",
    [
        "1/0",
        "-1/10",
        "1/-10",
        "nan/10",
        "inf/10",
        "1/inf",
        "1e309/10",
        "1/1e309",
        "1/10/3",
    ],
)
def test_calculate_depreciation_factor_rejects_invalid_numeric_ranges(value):
    with pytest.raises(ValueError):
        calculate_depreciation_factor(value)


def test_calculate_depreciation_factor_rejects_very_long_numeric_input():
    with pytest.raises(ValueError):
        calculate_depreciation_factor(f"{'9' * 10000}/10")


@given(
    st.one_of(
        st.none(),
        st.booleans(),
        st.integers(),
        st.floats(allow_nan=True),
        st.binary(),
        st.lists(st.text()),
        st.dictionaries(st.text(), st.text()),
    )
)
def test_calculate_depreciation_factor_rejects_non_strings(value):
    with pytest.raises(TypeError):
        calculate_depreciation_factor(value)


@given(
    st.sampled_from(tuple(CONDITION_MULTIPLIERS.items())),
    st.text(alphabet=" \t\n\r", max_size=5),
    st.text(alphabet=" \t\n\r", max_size=5),
)
def test_lookup_condition_multiplier_is_case_and_whitespace_insensitive(
    condition_and_multiplier, prefix, suffix
):
    condition, expected = condition_and_multiplier
    assert lookup_condition_multiplier(
        f"{prefix}{condition.lower()}{suffix}"
    ) == expected


@given(
    st.text(max_size=500).filter(
        lambda value: value.strip().upper() not in CONDITION_MULTIPLIERS
    )
)
def test_lookup_condition_multiplier_rejects_unknown_conditions(value):
    with pytest.raises(ValueError):
        lookup_condition_multiplier(value)


def test_lookup_condition_multiplier_rejects_very_long_unknown_value():
    with pytest.raises(ValueError):
        lookup_condition_multiplier("UNKNOWN" * 10000)


@given(
    st.one_of(
        st.none(),
        st.booleans(),
        st.integers(),
        st.floats(allow_nan=True),
        st.binary(),
        st.lists(st.text()),
        st.dictionaries(st.text(), st.text()),
    )
)
def test_lookup_condition_multiplier_rejects_non_strings(value):
    with pytest.raises(TypeError):
        lookup_condition_multiplier(value)