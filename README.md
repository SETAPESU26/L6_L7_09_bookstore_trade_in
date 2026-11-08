# Bookstore Trade-In Labs

This repository contains two Python labs for a bookstore trade-in workflow:
Lab 6 implements buyback payouts and scanner calibration, and Lab 7 exercises
ISBN formatting, depreciation, and condition multipliers with property-based
tests.

## Features

- Calculates buyback values for paperback, hardcover, and textbook batches.
- Accounts for condition, missing pages, counterfeit alerts, store credit, and
  audit thresholds.
- Flags scanner devices with consecutive high misread rates.
- Extracts fields from ISBN-10 strings, calculates depreciation factors, and
  looks up condition multipliers.
- Uses Hypothesis to explore normal, malformed, boundary, Unicode, and
  incorrectly typed inputs for the Lab 7 processor.

## Project structure

| Path | Purpose |
|---|---|
| `Lab 6/bookstore_trade_in.py` | Lab 6 buyback and scanner functions |
| `Lab 6/test_bookstore_trade.py` | Lab 6 functional and branch-coverage tests |
| `Lab 6/README.md` | Lab 6 instructions |
| `Lab 7/processor.py` | Lab 7 input processing functions and interactive entry point |
| `Lab 7/test_processor.py` | Hypothesis properties and edge-case tests |
| `Lab 7/README.md` | Lab 7 instructions |
| `LAB7_REPORT.md` | Fuzz-testing findings and results |
| `requirements-dev.txt` | Test dependencies |
| `screenshots/` | Screenshot evidence status |

## Install

Use Python 3 and install the development/test dependencies from the repository
root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

The requirements are Hypothesis, pytest, and pytest-cov. The application
functions have no third-party runtime dependencies.

## Run the application

Run the interactive Lab 7 processor from the repository root:

```powershell
python "Lab 7\processor.py"
```

It prompts for an ISBN-10 string, an age/lifespan ratio, and a condition code.
For example, enter `0-306-40615-2`, `3/10`, and `MINT`.

## Run tests

Run the complete test suite:

```powershell
python -m pytest -v
```

Run the required Lab 7 fuzz/property tests only:

```powershell
python -m pytest "Lab 7\test_processor.py" -v
```

Measure Lab 6 line and branch coverage from its folder:

```powershell
Set-Location "Lab 6"
python -m pytest -v --cov=bookstore_trade_in --cov-branch --cov-report=term-missing
```

## Bugs found and fixes

The initial Hypothesis run exposed malformed ISBNs that caused indexing errors
or were accepted despite invalid length/characters, non-string inputs that
raised incidental `AttributeError`s, zero lifespan division, unbounded negative
age/lifespan values, non-finite depreciation values, and unknown condition
codes that leaked `KeyError`. Lab 7 now validates these inputs and raises
documented `TypeError` or `ValueError` exceptions. The interactive entry point
prints validation messages instead of a traceback for invalid user input.

The existing Lab 6 application was retained unchanged. Its starter coverage
TODO was completed with tests covering payout branches, rejections, audit
status, and scanner calibration.

## Testing results

The expanded pre-fix Lab 7 suite recorded **19 failures and 6 passes**. After
the fixes, Lab 7 passed **30 tests**. Lab 6 passed **12 tests**, with **100%
line and branch coverage** for `bookstore_trade_in.py`. The complete suite and
application were also run locally; detailed results and screenshot
limitations are in [LAB7_REPORT.md](./LAB7_REPORT.md).

## Scope and limitations

`verify_isbn10_format` checks the ISBN-10 character format and extracts the
requested fields; it does not calculate or verify the ISBN checksum. The
repository does not include the referenced Lab 7 handout, so the existing
processor implementation and Lab 7 README were used as the available source
of contract details.
