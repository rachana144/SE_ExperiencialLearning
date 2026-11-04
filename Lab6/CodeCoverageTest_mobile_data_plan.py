"""Lab 6 - Code (line) coverage tests for mobile_data_plan.py
Author: Rachana K (PES1UG24CS354)

Run:
    coverage run -m pytest CodeCoverageTest_mobile_data_plan.py
    coverage report -m
"""
import pytest
from mobile_data_plan import overage_charge, recharge_allowed, validity_status


# ---------------- overage_charge ----------------
def test_within_included_data():
    assert overage_charge("standard", 3, False, False) == 0


def test_unknown_plan_raises():
    with pytest.raises(ValueError, match="unknown plan"):
        overage_charge("gold", 3, False, False)


def test_negative_usage_raises():
    with pytest.raises(ValueError, match="invalid data usage"):
        overage_charge("basic", -1, False, False)


def test_loyal_non_premium_gets_bonus_gb():
    # basic = 2GB + 1 loyalty GB = 3GB; usage 3 -> no extra
    assert overage_charge("basic", 3, False, True) == 0


def test_normal_overage_domestic():
    # extra = 4 - 2 = 2 GB @ 15
    assert overage_charge("basic", 4, False, False) == 30


def test_normal_overage_roaming():
    # extra = 4 - 2 = 2 GB @ 40
    assert overage_charge("basic", 4, True, False) == 80


def test_heavy_overage_domestic():
    # extra = 20 - 5 = 15 GB, rate 15 + 10 = 25
    assert overage_charge("standard", 20, False, False) == 15 * 25


def test_heavy_overage_roaming():
    # extra = 15 GB, rate 40 + 10 + 5 = 55
    assert overage_charge("standard", 20, True, False) == 15 * 55


# ---------------- recharge_allowed ----------------
def test_recharge_allowed():
    assert recharge_allowed(500, 1, False) is True


def test_recharge_kyc_pending_small_amount():
    assert recharge_allowed(200, 0, True) is True


def test_recharge_amount_too_high():
    assert recharge_allowed(2500, 0, False) is False


# ---------------- validity_status ----------------
def test_validity_active_prepaid():
    assert validity_status(5, True, False) == "active"


def test_validity_grace_postpaid():
    assert validity_status(0, False, False) == "grace"


def test_validity_expired_with_addon():
    assert validity_status(-20, False, True) == "expired"
