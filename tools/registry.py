from tools.convert_metric import CONVERT_METRIC_TOOL, convert_metric

TOOLS = [CONVERT_METRIC_TOOL]


def run_tool(name: str, tool_input: dict[str, object]) -> str:
    print("run_tool")
    if name == "convert_metric":
        result = convert_metric(
            float(str(tool_input["amount"])),
            str(tool_input["source_unit"]),
            str(tool_input["destination_unit"]),
        )
        return (
            f"{result:g} {tool_input['destination_unit']}"
            if result is not None
            else "Unsupported conversion."
        )
    return f"Unknown tool: {name}"
