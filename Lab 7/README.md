# L6_L7_09 — Bookstore Trade-In

Lab 7: Fuzz Testing with Hypothesis

## About

This lab uses Hypothesis property-based tests to exercise ISBN-10 format
extraction, book depreciation ratios, and condition multiplier lookups. The
processor validates the expected input types and value ranges; invalid values
raise `TypeError` or `ValueError`.

## Files

| File | Description |
|------|-------------|
| `processor.py` | Validated processing functions and interactive entry point |
| `test_processor.py` | Hypothesis properties and deterministic boundary tests |

Install dependencies from the repository root with
`python -m pip install -r requirements-dev.txt`. Run these tests from the
repository root:

```powershell
python -m pytest "Lab 7\test_processor.py" -v
```

The repository does not include the referenced lab handout. The test
properties follow the function behavior and examples in `processor.py` and
this README. ISBN handling validates format and extracts the check character;
it does not verify the ISBN checksum.