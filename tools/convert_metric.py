from anthropic.types import ToolParam

CONVERT_METRIC_TOOL: ToolParam = {
    "name": "convert_metric",
    "description": "Convert a measurement between metric units, e.g. grams to kilograms.",
    "input_schema": {
        "type": "object",
        "properties": {
            "amount": {"type": "number"},
            "source_unit": {"type": "string", "enum": ["g", "kg"]},
            "destination_unit": {"type": "string", "enum": ["kg", "g"]},
        },
        "required": ["amount", "source_unit", "destination_unit"],
    },
}


def convert_metric(
    amount: float, source_unit: str, destination_unit: str
) -> float | None:
    print("convert_metric")
    if source_unit == "g" and destination_unit == "kg":
        return amount / 1000
    if source_unit == "kg" and destination_unit == "g":
        return amount * 1000
    return None
