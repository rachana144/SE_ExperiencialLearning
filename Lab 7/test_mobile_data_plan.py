"""Lab 7 - Fuzz testing with Hypothesis
Author: Rachana K (PES1UG24CS354)

Run:
    python -m pytest test_mobile_data_plan.py
"""
import math

from hypothesis import given, strategies as st
from mobile_data_plan import parse_plan, usage_average, payable_bill


# ---------------------------------------------------------------
# 1. Crash fuzzing: any str / None input must never raise.
# ---------------------------------------------------------------
@given(st.text() | st.none())
def test_parse_plan_no_crash(s):
    try:
        parse_plan(s)
    except Exception as e:
        assert False, f"parse_plan crashed with: {e!r} for input {s!r}"


@given(st.text() | st.none())
def test_usage_average_no_crash(s):
    try:
        usage_average(s)
    except Exception as e:
        assert False, f"usage_average crashed with: {e!r} for input {s!r}"


@given(st.text() | st.none())
def test_payable_bill_no_crash(s):
    try:
        payable_bill(s)
    except Exception as e:
        assert False, f"payable_bill crashed with: {e!r} for input {s!r}"


# ---------------------------------------------------------------
# 2. Fuzzing with non-string types (ints, floats, lists, bytes...)
# ---------------------------------------------------------------
any_value = st.one_of(st.integers(), st.floats(), st.binary(),
                      st.lists(st.integers()), st.booleans(), st.none())


@given(any_value)
def test_parse_plan_non_string_no_crash(v):
    try:
        parse_plan(v)
    except Exception as e:
        assert False, f"parse_plan crashed with: {e!r} for input {v!r}"


@given(any_value)
def test_usage_average_non_string_no_crash(v):
    try:
        usage_average(v)
    except Exception as e:
        assert False, f"usage_average crashed with: {e!r} for input {v!r}"


@given(any_value)
def test_payable_bill_non_string_no_crash(v):
    try:
        payable_bill(v)
    except Exception as e:
        assert False, f"payable_bill crashed with: {e!r} for input {v!r}"


# ---------------------------------------------------------------
# 3. Property tests on structured, *valid* inputs
# ---------------------------------------------------------------
plan_names = st.text(alphabet=st.characters(whitelist_categories=("Lu", "Ll")),
                     min_size=1, max_size=20)


@given(plan_names, st.floats(min_value=0, max_value=1e6))
def test_parse_plan_valid_roundtrip(name, gb):
    result = parse_plan(f"{name}:{gb}")
    assert result is not None
    assert result[0] == name.title()
    assert result[1] == gb


@given(st.lists(st.integers(min_value=0, max_value=10**9), min_size=1, max_size=50))
def test_usage_average_between_min_and_max(values):
    result = usage_average(",".join(str(v) for v in values))
    assert result == sum(values) // len(values)
    assert min(values) <= result <= max(values)


@given(st.floats(min_value=0, max_value=1e9), st.floats(min_value=0, max_value=1e9))
def test_payable_bill_never_negative_and_finite(bill, discount):
    result = payable_bill(f"{bill}|{discount}")
    assert result is not None
    assert math.isfinite(result)
    assert result >= 0


# ---------------------------------------------------------------
# 4. Specific edge cases found by fuzzing
# ---------------------------------------------------------------
def test_parse_plan_rejects_bad_input():
    for bad in ["", "standard", "standard:", ":5", "a:b:c", "standard:abc",
                "standard:nan", "standard:inf", "standard:-5", None, 123]:
        assert parse_plan(bad) is None, bad


def test_usage_average_rejects_bad_input():
    for bad in ["", ",", "1,,3", "one,two", "1,2,", "-5,10", "1.5,2", None, 123]:
        assert usage_average(bad) is None, bad


def test_payable_bill_rejects_bad_input():
    for bad in ["", "399", "399|", "|50", "a|b", "nan|0", "inf|0", "100|inf",
                "-100|0", "100|-5", "1|2|3", "1.7e308|0", None, 123]:
        assert payable_bill(bad) is None, bad


def test_valid_examples():
    assert parse_plan("standard:5") == ("Standard", 5.0)
    assert parse_plan("  basic : 2.5 ") == ("Basic", 2.5)
    assert usage_average("300,450,800") == 516
    assert payable_bill("399|50") == 399 * 1.18 - 50
    assert payable_bill("10|500") == 0
