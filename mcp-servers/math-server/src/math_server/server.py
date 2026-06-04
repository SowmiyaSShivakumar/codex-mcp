from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from .operations import add, divide, multiply, subtract

mcp = FastMCP("math-server")


def _json(data: dict) -> str:
    return json.dumps(data)


@mcp.tool("add")
def add_numbers(a: float, b: float) -> str:
    """Add two numbers and return a JSON result."""
    return _json({"operation": "add", "a": a, "b": b, "result": add(a, b)})


@mcp.tool("subtract")
def subtract_numbers(a: float, b: float) -> str:
    """Subtract b from a and return a JSON result."""
    return _json({"operation": "subtract", "a": a, "b": b, "result": subtract(a, b)})


@mcp.tool()
def multiply_numbers(a: float, b: float) -> str:
    """Multiply two numbers and return a JSON result."""
    return _json({"operation": "multiply", "a": a, "b": b, "result": multiply(a, b)})


@mcp.tool()
def divide_numbers(a: float, b: float) -> str:
    """Divide a by b and return a JSON result."""
    result = divide(a, b)
    return _json({"operation": "divide", "a": a, "b": b, "result": result})


def main() -> None:
    mcp.run()
