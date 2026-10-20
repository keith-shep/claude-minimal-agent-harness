from typing import Literal

from anthropic import beta_tool


@beta_tool
def convert_metric(
    amount: float,
    source_unit: Literal["g", "kg"],
    destination_unit: Literal["g", "kg"],
) -> str:
    """Convert a measurement between metric units in either direction, e.g. grams to kilograms."""
    print(f"running convert_metric({amount}, {source_unit}, {destination_unit})")
    if source_unit == "g" and destination_unit == "kg":
        return f"{amount / 1000:g} kg"
    if source_unit == "kg" and destination_unit == "g":
        return f"{amount * 1000:g} g"
    return "Unsupported conversion."
