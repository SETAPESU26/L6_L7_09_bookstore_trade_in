# L6_L7_09 — Bookstore Trade-In

Lab 6: Code and Branch Coverage

## About

A small Python module that evaluates used book trade-in values across formats, wear conditions, and counterfeit alerts, and monitors optical barcode scanners for misread rates.

## Files

| File | Description |
|------|-------------|
| `bookstore_trade_in.py` | The module under test |
| `test_bookstore_trade.py` | Functional and branch-coverage tests |

Keep all your Lab 6 work in this `LAB6` folder. Lab 7 will be added to this repo later.

From this folder, install the repository's development dependencies and run
the tests with branch coverage:

```powershell
python -m pip install -r ..\requirements-dev.txt
python -m pytest -v --cov=bookstore_trade_in --cov-branch --cov-report=term-missing
```

The test suite covers the buyback payout/status branches and scanner
calibration outcomes. Refer to the lab handout for the original assignment
instructions.