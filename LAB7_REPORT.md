# Lab 7 Fuzz Testing Report

## Summary

Hypothesis property-based tests were used to examine the three public
functions in `Lab 7/processor.py`. The first expanded run against the original
implementation failed 19 of 25 collected tests. After validation fixes, all 30
Lab 7 tests passed. The Lab 6 regression suite passes 12 tests and measures
100% line and branch coverage for its application module.

The referenced Lab 7 handout was not present in the repository. The available
Lab 7 README and starter implementation were used to derive the behavior
contracts, preserving the existing return formats and condition values.

## What fuzz testing is

Fuzz testing supplies many generated values to software to expose failures
that a small set of hand-written examples may miss. Property-based testing
focuses on expected invariants—for example, a depreciation factor remains
within its documented range—rather than asserting that every arbitrary input
must succeed.

## Why Hypothesis

Hypothesis integrates with pytest and generates and shrinks input values. A
shrunk counterexample makes a failure easier to reproduce. The tests use
`@given` with `hypothesis.strategies as st` to generate valid values and
malformed text, Unicode, empty values, `None`, and incorrect data types.
Deterministic cases supplement generation for zero denominators, non-finite
numbers, very long strings, and floating-point boundaries.

## Functions tested

| Function | Intended behavior tested |
|---|---|
| `verify_isbn10_format` | Accepts a ten-character ISBN-10 body (nine ASCII digits followed by a digit or X, with optional hyphens and surrounding whitespace) and returns the original group/first-digit/check-character summary format. |
| `calculate_depreciation_factor` | Accepts `age/lifespan` numeric text for finite age >= 0 and finite lifespan > 0, then returns the existing rounded ratio with a 0.1 floor. |
| `lookup_condition_multiplier` | Trims and case-normalizes one of the five supported condition codes and returns its existing multiplier. |

Invalid input types raise `TypeError`; malformed strings, invalid numeric
ranges, and unsupported condition codes raise `ValueError`.

## Initial failing tests

Against the original code, the expanded baseline had **19 failures and 6
passes**:

- ISBN `""` reproduced an `IndexError`. Inputs with too few or too many
  digits, a misplaced `X`, full-width Unicode digits, or 10,000 digits were
  accepted or processed without the required format check.
- `None` passed to each of the three functions produced an incidental
  `AttributeError` (`replace`, `split`, or `strip`).
- The ratio `1/0` raised `ZeroDivisionError`.
- Negative age/lifespan and `nan`, `inf`, `1e309/10`, and `1/1e309` were not
  rejected consistently; some returned values outside the expected range.
- An empty condition string raised `KeyError` instead of a clear validation
  error.

These are observed test results, not simulated output. The original source
was available locally and was run by the failing tests before it was changed.

## Fixes implemented

- Added explicit string type checks to each processor function.
- Added an ISBN-10 body format check using ASCII digits and a final digit or
  `X`, while preserving the original field-extraction output. No checksum
  calculation was added because the starter function did not perform one.
- Required exactly one age/lifespan separator, numeric finite values,
  nonnegative age, and positive lifespan before calculating depreciation.
- Added a value check before condition dictionary lookup so unknown codes
  produce a deliberate `ValueError`.
- Updated the interactive entry point to display validation messages for
  invalid values rather than print tracebacks.
- Completed the existing Lab 6 test TODO without changing its application
  code. The Lab 6 tests cover payout and scanner branches.

## Before-and-after test results

| Run | Result |
|---|---|
| Lab 7 expanded suite, original processor | 19 failed, 6 passed (25 collected) |
| Lab 7 suite, validated processor | 30 passed |
| Lab 6 suite | 12 passed; 100% line and branch coverage |
| Complete repository suite | 42 passed |
| Interactive Lab 7 sample | Completed with `Group 306: Starts 0, Checksum 2`, depreciation `0.7`, multiplier `1.25` |
| Interactive malformed ISBN | Printed a clear validation message and exited without a traceback |

## Screenshot evidence

The original buggy behavior and final passing test/application output were
executed in the terminal during this work. This session does not provide a
desktop or terminal screenshot-capture facility, so no screenshot images were
created; `screenshots/README.md` records that limitation. No screenshots or
test outputs have been fabricated.

## Limitations

- The ISBN function validates character format but does not calculate or
  verify the ISBN-10 checksum.
- The Lab 7 handout referred to by the repository README was not included in
  the repository.
- Genuine screenshot images could not be captured in this execution
  environment.
