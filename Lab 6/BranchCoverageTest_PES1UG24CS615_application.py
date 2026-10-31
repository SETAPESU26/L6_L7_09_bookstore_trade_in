import pytest

from bookstore_trade_in import (
    process_book_buybacks,
    inspect_scanner_calibration
)


# Input validation tests

def test_invalid_batches_type():
    with pytest.raises(ValueError):
        process_book_buybacks("invalid", 5.0)


def test_negative_store_credit_bonus():
    with pytest.raises(ValueError):
        process_book_buybacks([], -5.0)


# Book format tests

def test_textbook_format():
    result = process_book_buybacks([
        {"intake_approved": True, "format": "textbook",
         "books": [{"condition": "good"}]}
    ], 5.0)
    assert result["total_payout"] == 40.0


def test_hardcover_format():
    result = process_book_buybacks([
        {"intake_approved": True, "format": "hardcover",
         "books": [{"condition": "good"}]}
    ], 5.0)
    assert result["total_payout"] == 15.0


def test_paperback_format():
    result = process_book_buybacks([
        {"intake_approved": True, "format": "paperback",
         "books": [{"condition": "good"}]}
    ], 5.0)
    assert result["total_payout"] == 8.0


def test_unsupported_format():
    result = process_book_buybacks([
        {"intake_approved": True, "format": "magazine",
         "books": []}
    ], 5.0)
    assert result["status"] == "ZERO_CREDIT"


# Intake approval tests

def test_approved_batch():
    result = process_book_buybacks([
        {"intake_approved": True, "format": "paperback",
         "books": [{"condition": "good"}]}
    ], 5.0)
    assert result["status"] == "COMPLETED"


def test_unapproved_batch():
    result = process_book_buybacks([
        {"intake_approved": False, "format": "paperback",
         "books": [{"condition": "good"}]}
    ], 5.0)
    assert result["status"] == "ZERO_CREDIT"


# Missing pages tests

def test_missing_pages_positive():
    result = process_book_buybacks([
        {"intake_approved": True, "format": "paperback",
         "books": [{"missing_pages": 2}]}
    ], 5.0)
    assert result["status"] == "ZERO_CREDIT"


def test_no_missing_pages():
    result = process_book_buybacks([
        {"intake_approved": True, "format": "paperback",
         "books": [{"missing_pages": 0}]}
    ], 5.0)
    assert result["total_payout"] == 8.0


# Counterfeit tests

def test_counterfeit_paperback():
    result = process_book_buybacks([
        {"intake_approved": True, "format": "paperback",
         "books": [{"counterfeit": True}]}
    ], 5.0)
    assert result["status"] == "ZERO_CREDIT"


def test_counterfeit_textbook_stops_batch():
    result = process_book_buybacks([
        {"intake_approved": True, "format": "textbook",
         "books": [
             {"counterfeit": True},
             {"condition": "mint"}
         ]}
    ], 5.0)
    assert result["status"] == "ZERO_CREDIT"


def test_non_counterfeit_book():
    result = process_book_buybacks([
        {"intake_approved": True, "format": "paperback",
         "books": [{"counterfeit": False, "condition": "good"}]}
    ], 5.0)
    assert result["total_payout"] == 8.0


# Condition tests

def test_mint_condition():
    result = process_book_buybacks([
        {"intake_approved": True, "format": "paperback",
         "books": [{"condition": "mint"}]}
    ], 5.0)
    assert result["total_payout"] == 10.0


def test_poor_condition():
    result = process_book_buybacks([
        {"intake_approved": True, "format": "paperback",
         "books": [{"condition": "poor"}]}
    ], 5.0)
    assert result["total_payout"] == 3.2


def test_good_condition():
    result = process_book_buybacks([
        {"intake_approved": True, "format": "paperback",
         "books": [{"condition": "good"}]}
    ], 5.0)
    assert result["total_payout"] == 8.0


# Store credit tests

def test_credit_bonus_enabled():
    result = process_book_buybacks([
        {"intake_approved": True, "format": "paperback",
         "payout_in_credit": True,
         "books": [{"condition": "good"}]}
    ], 5.0)
    assert result["total_payout"] == 13.0


def test_credit_bonus_disabled():
    result = process_book_buybacks([
        {"intake_approved": True, "format": "paperback",
         "payout_in_credit": False,
         "books": [{"condition": "good"}]}
    ], 5.0)
    assert result["total_payout"] == 8.0


# Final payout status tests

def test_audit_rejected_more_than_four_items():
    result = process_book_buybacks([
        {"intake_approved": True, "format": "paperback",
         "books": [{"missing_pages": 1} for _ in range(5)]}
    ], 5.0)
    assert result["status"] == "AUDIT_REJECTED"


def test_four_rejected_items_not_audit_rejected():
    result = process_book_buybacks([
        {"intake_approved": True, "format": "paperback",
         "books": [{"missing_pages": 1} for _ in range(4)]}
    ], 5.0)
    assert result["status"] == "ZERO_CREDIT"


def test_zero_payout():
    result = process_book_buybacks([
        {"intake_approved": True, "format": "hardcover",
         "books": []}
    ], 5.0)
    assert result["status"] == "ZERO_CREDIT"


def test_completed_payout():
    result = process_book_buybacks([
        {"intake_approved": True, "format": "hardcover",
         "books": [{"condition": "good"}]}
    ], 5.0)
    assert result["status"] == "COMPLETED"


# Scanner calibration tests

def test_empty_scanner_matrix():
    assert inspect_scanner_calibration([]) == "NO_DATA"


def test_scanner_with_empty_readings():
    assert inspect_scanner_calibration([[]]) == "CALIBRATED"


def test_scanner_error_rate_above_five():
    assert inspect_scanner_calibration([[6]]) == "CALIBRATED"


def test_scanner_error_rate_equal_to_five():
    assert inspect_scanner_calibration([[5]]) == "CALIBRATED"


def test_scanner_two_consecutive_errors():
    assert inspect_scanner_calibration([[6, 7]]) == "RECALIBRATE"


def test_scanner_streak_reset():
    assert inspect_scanner_calibration([[6, 2, 7]]) == "CALIBRATED"


def test_scanner_separate_devices():
    assert inspect_scanner_calibration([[6], [7]]) == "CALIBRATED"


def test_scanner_multiple_normal_readings():
    assert inspect_scanner_calibration([[1, 2, 3, 4, 5]]) == "CALIBRATED"
