from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from .conversions import (
    bytes_to_megabytes,
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    feet_to_meters,
    megabytes_to_bytes,
    meters_to_feet,
)

mcp = FastMCP("unit-converter")


def _ok(data: dict) -> str:
    return json.dumps(data)


# ── Temperature ──────────────────────────────────────────────────────────────

@mcp.tool()
def convert_celsius_to_fahrenheit(celsius: float) -> str:
    """Convert a temperature from Celsius to Fahrenheit.

    Args:
        celsius: Temperature in degrees Celsius.

    Returns:
        JSON with the original value and the converted Fahrenheit result.
    """
    result = celsius_to_fahrenheit(celsius)
    return _ok({"input_celsius": celsius, "output_fahrenheit": round(result, 6)})


@mcp.tool()
def convert_fahrenheit_to_celsius(fahrenheit: float) -> str:
    """Convert a temperature from Fahrenheit to Celsius.

    Args:
        fahrenheit: Temperature in degrees Fahrenheit.

    Returns:
        JSON with the original value and the converted Celsius result.
    """
    result = fahrenheit_to_celsius(fahrenheit)
    return _ok({"input_fahrenheit": fahrenheit, "output_celsius": round(result, 6)})


# ── Length ───────────────────────────────────────────────────────────────────

@mcp.tool()
def convert_meters_to_feet(meters: float) -> str:
    """Convert a length from meters to feet.

    Args:
        meters: Length in meters.

    Returns:
        JSON with the original value and the converted feet result.
    """
    result = meters_to_feet(meters)
    return _ok({"input_meters": meters, "output_feet": round(result, 6)})


@mcp.tool()
def convert_feet_to_meters(feet: float) -> str:
    """Convert a length from feet to meters.

    Args:
        feet: Length in feet.

    Returns:
        JSON with the original value and the converted meters result.
    """
    result = feet_to_meters(feet)
    return _ok({"input_feet": feet, "output_meters": round(result, 6)})


# ── Digital storage ───────────────────────────────────────────────────────────

@mcp.tool()
def convert_bytes_to_megabytes(num_bytes: float) -> str:
    """Convert a data size from bytes to megabytes (1 MB = 1024² bytes).

    Args:
        num_bytes: Size in bytes.

    Returns:
        JSON with the original value and the converted megabytes result.
    """
    result = bytes_to_megabytes(num_bytes)
    return _ok({"input_bytes": num_bytes, "output_megabytes": round(result, 9)})


@mcp.tool()
def convert_megabytes_to_bytes(megabytes: float) -> str:
    """Convert a data size from megabytes to bytes (1 MB = 1024² bytes).

    Args:
        megabytes: Size in megabytes.

    Returns:
        JSON with the original value and the converted bytes result.
    """
    result = megabytes_to_bytes(megabytes)
    return _ok({"input_megabytes": megabytes, "output_bytes": result})
