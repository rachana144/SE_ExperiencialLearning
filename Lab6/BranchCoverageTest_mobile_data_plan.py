"""Lab 6 - Branch coverage tests for mobile_data_plan.py
Author: Rachana K (PES1UG24CS354)

Run:
    coverage run --branch -m pytest BranchCoverageTest_mobile_data_plan.py
    coverage report -m
"""
import pytest
from mobile_data_plan import overage_charge, recharge_allowed, validity_status


# ================= overage_charge =================
# Guard clauses: plan not in table / negative usage
def test_unknown_plan_raises():
    with pytest.raises(ValueError, match="unknown plan"):
        overage_charge("gold", 3, False, False)


def test_negative_usage_raises():
    with pytest.raises(ValueError, match="invalid data usage"):
        overage_charge("basic", -1, False, False)


def test_zero_usage_is_valid():
    # data_gb < 0 False branch (boundary 0)
    assert overage_charge("basic", 0, False, False) == 0


# is_loyal and plan != "premium": True / False(not loyal) / False(premium)
def test_loyal_non_premium_gets_bonus_gb():
    assert overage_charge("basic", 3, False, True) == 0      # 2 + 1 = 3 GB


def test_loyal_non_premium_overage_after_bonus():
    assert overage_charge("basic", 4, False, True) == 15     # extra = 1


def test_not_loyal_no_bonus():
    assert overage_charge("basic", 3, False, False) == 15    # extra = 1


def test_loyal_premium_gets_no_bonus():
    assert overage_charge("premium", 11, False, True) == 15  # 10 GB only, extra = 1


# extra <= 0: True (equal / below) and False
def test_usage_below_included():
    assert overage_charge("standard", 3, False, False) == 0


def test_usage_exactly_included():
    assert overage_charge("standard", 5, True, False) == 0


# is_roaming True / False for the base rate
def test_domestic_rate():
    assert overage_charge("basic", 4, False, False) == 2 * 15


def test_roaming_rate():
    assert overage_charge("basic", 4, True, False) == 2 * 40


# extra > 10: boundary False (exactly 10), True domestic, True roaming
def test_extra_exactly_ten_no_surcharge_domestic():
    assert overage_charge("basic", 12, False, False) == 10 * 15


def test_extra_exactly_ten_no_surcharge_roaming():
    assert overage_charge("basic", 12, True, False) == 10 * 40


def test_extra_above_ten_domestic_surcharge():
    # extra = 11, rate = 15 + 10
    assert overage_charge("basic", 13, False, False) == 11 * 25


def test_extra_above_ten_roaming_surcharge():
    # extra = 11, rate = 40 + 10 + 5
    assert overage_charge("basic", 13, True, False) == 11 * 55


@pytest.mark.parametrize("plan,included", [("basic", 2), ("standard", 5), ("premium", 10)])
def test_all_plans_boundary(plan, included):
    assert overage_charge(plan, included, False, False) == 0
    assert overage_charge(plan, included + 1, False, False) == 15


# ================= recharge_allowed =================
def test_recharge_normal_allowed():
    assert recharge_allowed(500, 1, False) is True


def test_recharge_kyc_pending_within_limit():
    assert recharge_allowed(200, 0, True) is True


def test_recharge_kyc_pending_over_limit():
    assert recharge_allowed(201, 0, True) is False


def test_recharge_kyc_pending_ignores_pending_recharges():
    assert recharge_allowed(100, 10, True) is True


def test_recharge_amount_over_2000_rejected():
    assert recharge_allowed(2001, 0, False) is False


def test_recharge_amount_exactly_2000_allowed():
    assert recharge_allowed(2000, 0, False) is True


def test_recharge_pending_exactly_two_allowed():
    assert recharge_allowed(500, 2, False) is True


def test_recharge_pending_three_rejected():
    assert recharge_allowed(500, 3, False) is False


# ================= validity_status =================
# prepaid (cutoff 0) / postpaid (cutoff 3) x add-on (+2)
def test_prepaid_active_at_cutoff():
    assert validity_status(0, True, False) == "active"


def test_prepaid_grace_just_below_cutoff():
    assert validity_status(-1, True, False) == "grace"


def test_prepaid_grace_lower_boundary():
    assert validity_status(-15, True, False) == "grace"


def test_prepaid_expired():
    assert validity_status(-16, True, False) == "expired"


def test_postpaid_active_at_cutoff():
    assert validity_status(3, False, False) == "active"


def test_postpaid_grace_just_below_cutoff():
    assert validity_status(2, False, False) == "grace"


def test_postpaid_grace_lower_boundary():
    assert validity_status(-12, False, False) == "grace"


def test_postpaid_expired():
    assert validity_status(-13, False, False) == "expired"


def test_prepaid_addon_active_at_cutoff():
    assert validity_status(2, True, True) == "active"


def test_prepaid_addon_grace():
    assert validity_status(1, True, True) == "grace"


def test_postpaid_addon_active_at_cutoff():
    assert validity_status(5, False, True) == "active"


def test_postpaid_addon_expired():
    assert validity_status(-11, False, True) == "expired"
