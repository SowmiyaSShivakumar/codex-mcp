"""Pure conversion functions — no I/O, no side effects."""

from __future__ import annotations


def celsius_to_fahrenheit(celsius: float) -> float:
    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    return (fahrenheit - 32) * 5 / 9


def meters_to_feet(meters: float) -> float:
    return meters * 3.28084


def feet_to_meters(feet: float) -> float:
    return feet / 3.28084


def bytes_to_megabytes(b: float) -> float:
    return b / (1024 ** 2)


def megabytes_to_bytes(mb: float) -> float:
    return mb * (1024 ** 2)
