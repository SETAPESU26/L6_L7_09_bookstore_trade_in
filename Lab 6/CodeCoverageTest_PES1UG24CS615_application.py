import pytest

from bookstore_trade_in import (
    process_book_buybacks,
    inspect_scanner_calibration
)


def test_invalid_batches():
    with pytest.raises(ValueError):
        process_book_buybacks("invalid", 5.0)


def test_negative_bonus():
    with pytest.raises(ValueError):
        process_book_buybacks([], -5.0)


def test_textbook_mint():
    result = process_book_buybacks([
        {
            "intake_approved": True,
            "format": "textbook",
            "books": [{"condition": "mint"}]
        }
    ], 5.0)
    assert result["total_payout"] == 50.0


def test_hardcover_poor():
    result = process_book_buybacks([
        {
            "intake_approved": True,
            "format": "hardcover",
            "books": [{"condition": "poor"}]
        }
    ], 5.0)
    assert result["total_payout"] == 6.0


def test_paperback_good():
    result = process_book_buybacks([
        {
            "intake_approved": True,
            "format": "paperback",
            "books": [{"condition": "good"}]
        }
    ], 5.0)
    assert result["total_payout"] == 8.0


def test_unapproved_batch():
    result = process_book_buybacks([
        {"intake_approved": False, "format": "paperback"}
    ], 5.0)
    assert result["status"] == "ZERO_CREDIT"


def test_invalid_format():
    result = process_book_buybacks([
        {
            "intake_approved": True,
            "format": "magazine",
            "books": []
        }
    ], 5.0)
    assert result["status"] == "ZERO_CREDIT"


def test_missing_pages():
    result = process_book_buybacks([
        {
            "intake_approved": True,
            "format": "paperback",
            "books": [{"missing_pages": 3}]
        }
    ], 5.0)
    assert result["status"] == "ZERO_CREDIT"


def test_counterfeit_paperback():
    result = process_book_buybacks([
        {
            "intake_approved": True,
            "format": "paperback",
            "books": [{"counterfeit": True}]
        }
    ], 5.0)
    assert result["status"] == "ZERO_CREDIT"


def test_counterfeit_textbook():
    result = process_book_buybacks([
        {
            "intake_approved": True,
            "format": "textbook",
            "books": [
                {"counterfeit": True},
                {"condition": "mint"}
            ]
        }
    ], 5.0)
    assert result["status"] == "ZERO_CREDIT"


def test_store_credit_bonus():
    result = process_book_buybacks([
        {
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": True,
            "books": [{"condition": "good"}]
        }
    ], 5.0)
    assert result["total_payout"] == 13.0


def test_audit_rejected():
    result = process_book_buybacks([
        {
            "intake_approved": True,
            "format": "paperback",
            "books": [
                {"missing_pages": 1},
                {"missing_pages": 2},
                {"missing_pages": 3},
                {"missing_pages": 4},
                {"missing_pages": 5}
            ]
        }
    ], 5.0)
    assert result["status"] == "AUDIT_REJECTED"


def test_empty_books():
    result = process_book_buybacks([
        {
            "intake_approved": True,
            "format": "hardcover",
            "books": []
        }
    ], 5.0)
    assert result["status"] == "ZERO_CREDIT"


def test_scanner_no_data():
    assert inspect_scanner_calibration([]) == "NO_DATA"


def test_scanner_recalibrate():
    assert inspect_scanner_calibration([[6, 7, 2]]) == "RECALIBRATE"


def test_scanner_calibrated():
    assert inspect_scanner_calibration([[2, 3, 4, 5]]) == "CALIBRATED"


def test_scanner_error_streak_reset():
    assert inspect_scanner_calibration([[6, 2, 7]]) == "CALIBRATED"
