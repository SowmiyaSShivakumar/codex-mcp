import unittest

from src.mcp_unit_converter.conversions import (
    bytes_to_megabytes,
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    feet_to_meters,
    megabytes_to_bytes,
    meters_to_feet,
)


class TestTemperature(unittest.TestCase):
    def test_celsius_to_fahrenheit_freezing(self):
        self.assertAlmostEqual(celsius_to_fahrenheit(0), 32.0)

    def test_celsius_to_fahrenheit_boiling(self):
        self.assertAlmostEqual(celsius_to_fahrenheit(100), 212.0)

    def test_celsius_to_fahrenheit_body(self):
        self.assertAlmostEqual(celsius_to_fahrenheit(37), 98.6, places=5)

    def test_celsius_to_fahrenheit_negative(self):
        self.assertAlmostEqual(celsius_to_fahrenheit(-40), -40.0)

    def test_fahrenheit_to_celsius_freezing(self):
        self.assertAlmostEqual(fahrenheit_to_celsius(32), 0.0)

    def test_fahrenheit_to_celsius_boiling(self):
        self.assertAlmostEqual(fahrenheit_to_celsius(212), 100.0)

    def test_roundtrip_temperature(self):
        original = 25.0
        self.assertAlmostEqual(fahrenheit_to_celsius(celsius_to_fahrenheit(original)), original)


class TestLength(unittest.TestCase):
    def test_meters_to_feet_one_meter(self):
        self.assertAlmostEqual(meters_to_feet(1), 3.28084, places=5)

    def test_meters_to_feet_zero(self):
        self.assertAlmostEqual(meters_to_feet(0), 0.0)

    def test_feet_to_meters_one_foot(self):
        self.assertAlmostEqual(feet_to_meters(1), 0.3048, places=4)

    def test_roundtrip_length(self):
        original = 10.0
        self.assertAlmostEqual(feet_to_meters(meters_to_feet(original)), original, places=5)


class TestDigitalStorage(unittest.TestCase):
    def test_bytes_to_megabytes_one_mb(self):
        self.assertAlmostEqual(bytes_to_megabytes(1_048_576), 1.0)

    def test_bytes_to_megabytes_zero(self):
        self.assertAlmostEqual(bytes_to_megabytes(0), 0.0)

    def test_megabytes_to_bytes_one_mb(self):
        self.assertAlmostEqual(megabytes_to_bytes(1), 1_048_576)

    def test_roundtrip_storage(self):
        original = 512.0
        self.assertAlmostEqual(megabytes_to_bytes(bytes_to_megabytes(original)), original)


if __name__ == "__main__":
    unittest.main()
