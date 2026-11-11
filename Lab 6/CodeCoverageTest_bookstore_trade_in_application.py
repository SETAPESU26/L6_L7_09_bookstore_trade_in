import pytest
from bookstore_trade_in import process_book_buybacks, inspect_scanner_calibration


def make_batch(books, fmt="paperback", approved=True, credit=False):
    return {
        "intake_approved": approved,
        "format": fmt,
        "payout_in_credit": credit,
        "books": books,
    }


def book(missing=0, condition="good", counterfeit=False):
    return {"missing_pages": missing, "condition": condition, "counterfeit": counterfeit}


# ---------- process_book_buybacks ----------

def test_single_paperback_good():
    result = process_book_buybacks([make_batch([book()])], 5.0)
    assert result["total_payout"] == 8.0
    assert result["status"] == "COMPLETED"


def test_invalid_batches_not_a_list():
    with pytest.raises(ValueError):
        process_book_buybacks("not a list", 5.0)


def test_unapproved_batch_skipped():
    result = process_book_buybacks([make_batch([book()], approved=False)], 5.0)
    assert result == {"total_payout": 0.0, "status": "ZERO_CREDIT"}


def test_textbook_good():
    result = process_book_buybacks([make_batch([book()], fmt="textbook")], 5.0)
    assert result["total_payout"] == 40.0
    assert result["status"] == "COMPLETED"


def test_hardcover_good():
    result = process_book_buybacks([make_batch([book()], fmt="hardcover")], 5.0)
    assert result["total_payout"] == 15.0


def test_unknown_format_rejected():
    result = process_book_buybacks([make_batch([book()], fmt="ebook")], 5.0)
    assert result == {"total_payout": 0.0, "status": "ZERO_CREDIT"}


def test_book_with_missing_pages_rejected():
    result = process_book_buybacks([make_batch([book(missing=2), book()])], 5.0)
    assert result["total_payout"] == 8.0
    assert result["status"] == "COMPLETED"


def test_counterfeit_paperback_gives_no_credit():
    result = process_book_buybacks([make_batch([book(counterfeit=True), book()])], 5.0)
    assert result["total_payout"] == 8.0


def test_counterfeit_textbook_wipes_batch_credit():
    batch = make_batch([book(), book(counterfeit=True), book()], fmt="textbook")
    result = process_book_buybacks([batch], 5.0)
    assert result == {"total_payout": 0.0, "status": "ZERO_CREDIT"}


def test_mint_condition_bonus():
    result = process_book_buybacks([make_batch([book(condition="mint")])], 5.0)
    assert result["total_payout"] == pytest.approx(10.0)


def test_poor_condition_discount():
    result = process_book_buybacks([make_batch([book(condition="poor")])], 5.0)
    assert result["total_payout"] == pytest.approx(3.2)


def test_payout_in_credit_adds_bonus():
    result = process_book_buybacks([make_batch([book()], credit=True)], 5.0)
    assert result["total_payout"] == 13.0


def test_audit_rejected_when_more_than_four_rejections():
    batch = make_batch([book(missing=1) for _ in range(5)])
    result = process_book_buybacks([batch], 5.0)
    assert result["status"] == "AUDIT_REJECTED"


# ---------- inspect_scanner_calibration ----------

def test_scanner_no_data():
    assert inspect_scanner_calibration([]) == "NO_DATA"


def test_scanner_recalibrate():
    assert inspect_scanner_calibration([[6, 7]]) == "RECALIBRATE"


def test_scanner_calibrated():
    assert inspect_scanner_calibration([[1, 2, 3]]) == "CALIBRATED"
