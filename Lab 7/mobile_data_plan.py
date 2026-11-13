import math


def parse_plan(text):
    """Parse 'plan:gb' (e.g. 'standard:5') -> ('Standard', 5.0).

    Returns None if the input is not a well-formed, finite, non-negative value.
    """
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 2:
        return None
    plan = parts[0].strip()
    if not plan:
        return None
    try:
        gb = float(parts[1].strip())
    except ValueError:
        return None
    if not math.isfinite(gb) or gb < 0:
        return None
    return plan.title(), gb


def usage_average(usage_csv):
    """Average of comma-separated daily usage (MB), e.g. '300,450,800' -> 516.

    Returns None for empty/non-integer/negative entries or non-string input.
    """
    if not isinstance(usage_csv, str):
        return None
    values = []
    for item in usage_csv.split(','):
        try:
            value = int(item.strip())
        except ValueError:
            return None
        if value < 0:
            return None
        values.append(value)
    if not values:
        return None
    return sum(values) // len(values)


def payable_bill(text):
    """Parse 'bill|discount' and return the payable amount after 18% tax.

    Returns None for malformed, negative or non-finite values (nan/inf/overflow).
    """
    if not isinstance(text, str):
        return None
    parts = text.split('|')
    if len(parts) != 2:
        return None
    try:
        bill = float(parts[0].strip())
        discount = float(parts[1].strip())
    except ValueError:
        return None
    if not (math.isfinite(bill) and math.isfinite(discount)):
        return None
    if bill < 0 or discount < 0:
        return None
    total = bill * 1.18 - discount
    if not math.isfinite(total):
        return None
    return max(total, 0)


def main():
    print("==== Running parse_plan ====")
    user_input = input("Enter plan:data in GB (e.g. standard:5): ")
    result = parse_plan(user_input)
    print("Plan and Data:", result if result is not None else "Invalid input")

    print("\n==== Running usage_average ====")
    user_input = input("Enter daily usage in MB as CSV (e.g. 300,450,800): ")
    result = usage_average(user_input)
    print("Average Usage:", result if result is not None else "Invalid input")

    print("\n==== Running payable_bill ====")
    user_input = input("Enter bill|discount (e.g. 399|50): ")
    result = payable_bill(user_input)
    print("Payable Bill:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()
