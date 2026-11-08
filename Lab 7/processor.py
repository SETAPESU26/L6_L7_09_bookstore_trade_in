import math
import re


CONDITION_MULTIPLIERS = {
    "MINT": 1.25,
    "LIKE_NEW": 1.00,
    "VERY_GOOD": 0.80,
    "GOOD": 0.60,
    "POOR": 0.30,
}


def verify_isbn10_format(isbn_str: str) -> str:
    """Extract the ISBN-10 group, first digit, and check character."""
    if not isinstance(isbn_str, str):
        raise TypeError("isbn_str must be a string")

    cleaned = isbn_str.replace("-", "").strip()
    if re.fullmatch(r"[0-9]{9}[0-9Xx]", cleaned) is None:
        raise ValueError("ISBN-10 must contain nine digits and a final digit or X")

    first_digit = int(cleaned[0])
    group_code = cleaned[1:4]
    check_char = cleaned[9].upper()
    return f"Group {group_code}: Starts {first_digit}, Checksum {check_char}"


def calculate_depreciation_factor(book_age_str: str) -> float:
    """Return a depreciation factor for a nonnegative age and positive lifespan."""
    if not isinstance(book_age_str, str):
        raise TypeError("book_age_str must be a string")

    values = book_age_str.split("/")
    if len(values) != 2:
        raise ValueError("Age and lifespan must be provided as age/lifespan")

    try:
        age, life = (float(value) for value in values)
    except ValueError as exc:
        raise ValueError("Age and lifespan must be numeric") from exc

    if not math.isfinite(age) or age < 0:
        raise ValueError("Age must be a finite, nonnegative number")
    if not math.isfinite(life) or life <= 0:
        raise ValueError("Lifespan must be a finite, positive number")

    depreciation = 1.0 - (age / life)
    return round(max(0.1, depreciation), 2)


def lookup_condition_multiplier(condition_code: str) -> float:
    """Return the trade-in multiplier for a recognized condition code."""
    if not isinstance(condition_code, str):
        raise TypeError("condition_code must be a string")

    grade = condition_code.strip().upper()
    if grade not in CONDITION_MULTIPLIERS:
        raise ValueError(f"Unknown condition code: {condition_code!r}")
    return CONDITION_MULTIPLIERS[grade]


def main():
    print("==== Running verify_isbn10_format ====")
    try:
        isbn_in = input("Enter ISBN-10 (e.g. 0-306-40615-2): ")
    except EOFError:
        print("No ISBN-10 input was provided.")
        return
    try:
        print(verify_isbn10_format(isbn_in))
    except ValueError as exc:
        print(f"Invalid ISBN-10: {exc}")
        return

    print("\n==== Running calculate_depreciation_factor ====")
    try:
        age_in = input("Enter age/lifespan in years (e.g. 3/10): ")
    except EOFError:
        print("No age/lifespan input was provided.")
        return
    try:
        print("Depreciation Factor:", calculate_depreciation_factor(age_in))
    except ValueError as exc:
        print(f"Invalid age/lifespan: {exc}")
        return

    print("\n==== Running lookup_condition_multiplier ====")
    try:
        cond_in = input("Enter condition (e.g. MINT, GOOD, POOR): ")
    except EOFError:
        print("No condition input was provided.")
        return
    try:
        print("Multiplier:", lookup_condition_multiplier(cond_in))
    except ValueError as exc:
        print(f"Invalid condition: {exc}")


if __name__ == "__main__":
    main()
