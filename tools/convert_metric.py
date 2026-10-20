from typing import Literal

from anthropic import beta_tool


@beta_tool
def convert_metric_tool(
    amount: float,
    source_unit: Literal["g", "kg"],
    destination_unit: Literal["g", "kg"],
) -> str:
    """Convert a measurement between metric units in either direction, e.g. grams to kilograms."""
    print(f"running convert_metric({amount}, {source_unit}, {destination_unit})")

    result = convert_metric(amount, source_unit, destination_unit)
    if result is None:
        return "Unsupported conversion."

    return f"{result} {destination_unit}"


def convert_metric(
    amount: float,
    source_unit: Literal["g", "kg"],
    destination_unit: Literal["g", "kg"],
) -> float | None:
    if source_unit == "g" and destination_unit == "kg":
        return amount / 1000
    if source_unit == "kg" and destination_unit == "g":
        return amount * 1000
    return None
