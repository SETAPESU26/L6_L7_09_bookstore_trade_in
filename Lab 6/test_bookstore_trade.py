import pytest
from bookstore_trade_in import process_book_buybacks, inspect_scanner_calibration


def test_single_paperback_good():
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": False,
            "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
        }
    ]
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 8.0
    assert result["status"] == "COMPLETED"


@pytest.mark.parametrize(
    ("batches", "bonus"),
    [
        ({}, 0.0),
        ([], -1.0),
    ],
)
def test_buybacks_reject_invalid_arguments(batches, bonus):
    with pytest.raises(ValueError):
        process_book_buybacks(batches, bonus)


def test_buybacks_apply_format_and_condition_values_and_defaults():
    result = process_book_buybacks(
        [
            {"intake_approved": True, "books": [{}]},
            {
                "intake_approved": True,
                "format": "textbook",
                "books": [{"condition": "good"}],
            },
            {
                "intake_approved": True,
                "format": "hardcover",
                "books": [{"condition": "mint"}],
            },
            {
                "intake_approved": True,
                "format": "paperback",
                "books": [{"condition": "poor"}],
            },
        ],
        5.0,
    )
    assert result == {"total_payout": 69.95, "status": "COMPLETED"}


def test_buybacks_skip_unapproved_and_reject_invalid_format_or_pages():
    result = process_book_buybacks(
        [
            {"format": "paperback", "books": [{"condition": "mint"}]},
            {
                "intake_approved": True,
                "format": "ebook",
                "books": [{"condition": "good"}],
            },
            {
                "intake_approved": True,
                "format": "paperback",
                "books": [{"missing_pages": 2}, {}],
            },
            {
                "intake_approved": True,
                "format": "paperback",
                "books": [{}],
            },
        ],
        0.0,
    )
    assert result == {"total_payout": 16.0, "status": "COMPLETED"}


def test_buybacks_handle_counterfeits_by_format():
    result = process_book_buybacks(
        [
            {
                "intake_approved": True,
                "format": "textbook",
                "books": [{"counterfeit": True}, {"condition": "mint"}],
            },
            {
                "intake_approved": True,
                "format": "paperback",
                "books": [{"counterfeit": True}, {}],
            },
        ],
        0.0,
    )
    assert result == {"total_payout": 8.0, "status": "COMPLETED"}


def test_buybacks_apply_credit_bonus_and_audit_rejection_threshold():
    result = process_book_buybacks(
        [
            {
                "intake_approved": True,
                "payout_in_credit": True,
                "books": [],
            },
            {
                "intake_approved": True,
                "format": "paperback",
                "books": [{}] + [{"missing_pages": 1}] * 5,
            },
        ],
        5.0,
    )
    assert result == {"total_payout": 13.0, "status": "AUDIT_REJECTED"}


@pytest.mark.parametrize(
    "batches",
    [
        [],
        [{"intake_approved": True, "books": []}],
        [
            {
                "intake_approved": True,
                "format": "textbook",
                "books": [{"counterfeit": True}],
            }
        ],
    ],
)
def test_buybacks_return_zero_credit_when_no_payout_is_earned(batches):
    assert process_book_buybacks(batches, 0.0) == {
        "total_payout": 0.0,
        "status": "ZERO_CREDIT",
    }


def test_scanner_reports_no_data_and_calibrated_readings():
    assert inspect_scanner_calibration([]) == "NO_DATA"
    assert inspect_scanner_calibration([[]]) == "CALIBRATED"
    assert inspect_scanner_calibration([[5, 6, 4], [6], [6]]) == "CALIBRATED"


def test_scanner_requests_recalibration_after_two_consecutive_misreads():
    assert inspect_scanner_calibration([[6, 6]]) == "RECALIBRATE"