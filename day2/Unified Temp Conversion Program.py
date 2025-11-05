#!/usr/bin/env python3
"""
unified_temp_converter.py
Convert temperatures between Celsius (C), Fahrenheit (F), Kelvin (K), and Rankine (R).

Usage (CLI):
  python unified_temp_converter.py 100 C F
  python unified_temp_converter.py -p 3 310.15 K C
  python unified_temp_converter.py --list

Interactive:
  python unified_temp_converter.py
"""

from __future__ import annotations
import argparse
import sys
import re

CANON_UNITS = {"C", "F", "K", "R"}

# Absolute zero in each scale
ABS_ZERO = {
    "C": -273.15,
    "F": -459.67,
    "K": 0.0,
    "R": 0.0,
}

# Common synonyms → canonical unit
UNIT_SYNONYMS = {
    "c": "C", "cel": "C", "cels": "C", "celsius": "C", "°c": "C", "degc": "C",
    "f": "F", "fahr": "F", "fahrenheit": "F", "°f": "F", "degf": "F",
    "k": "K", "kelvin": "K", "°k": "K",
    "r": "R", "rankine": "R", "°r": "R", "degR".lower(): "R"
}

def canonicalize_unit(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z°]", "", s)  # strip symbols except degree sign
    if s in UNIT_SYNONYMS:
        return UNIT_SYNONYMS[s]
    s_up = s.upper().replace("°", "")
    if s_up in CANON_UNITS:
        return s_up
    raise ValueError(f"Unrecognized unit '{s}' (try C, F, K, or R).")

def check_above_abs_zero(val: float, unit: str) -> None:
    if val < ABS_ZERO[unit] - 1e-12:
        raise ValueError(
            f"Value {val} {unit} is below absolute zero ({ABS_ZERO[unit]} {unit})."
        )

def to_kelvin(val: float, unit: str) -> float:
    if unit == "K":
        return val
    if unit == "C":
        return val + 273.15
    if unit == "F":
        return (val - 32.0) * 5.0/9.0 + 273.15
    if unit == "R":
        return val * 5.0/9.0
    raise ValueError(f"Unsupported unit '{unit}'")

def from_kelvin(k: float, unit: str) -> float:
    if unit == "K":
        return k
    if unit == "C":
        return k - 273.15
    if unit == "F":
        return (k - 273.15) * 9.0/5.0 + 32.0
    if unit == "R":
        return k * 9.0/5.0
    raise ValueError(f"Unsupported unit '{unit}'")

def convert(val: float, from_unit: str, to_unit: str) -> float:
    f = canonicalize_unit(from_unit)
    t = canonicalize_unit(to_unit)
    check_above_abs_zero(val, f)
    k = to_kelvin(val, f)
    return from_kelvin(k, t)

def format_out(val: float, unit: str, precision: int) -> str:
    # Add the degree symbol for C/F/R; Kelvin has no degree symbol.
    if unit in ("C", "F", "R"):
        return f"{val:.{precision}f} °{unit}"
    return f"{val:.{precision}f} {unit}"

def list_examples():
    examples = [
        ("100 C F", 100, "C", "F"),
        ("0 C K", 0, "C", "K"),
        ("32 F C", 32, "F", "C"),
        ("451 F K", 451, "F", "K"),
        ("300 K C", 300, "K", "C"),
        ("540 R C", 540, "R", "C"),
    ]
    lines = ["Examples:"]
    for label, v, u1, u2 in examples:
        try:
            out = convert(v, u1, u2)
            lines.append(f"  {label:<10} -> {out:.2f} {u2}")
        except Exception as e:
            lines.append(f"  {label:<10} -> error: {e}")
    return "\n".join(lines)

def run_cli():
    parser = argparse.ArgumentParser(
        description="Unified temperature converter (C, F, K, R).",
        add_help=True
    )
    parser.add_argument("value", type=float, nargs="?", help="numeric temperature")
    parser.add_argument("from_unit", type=str, nargs="?", help="source unit (C/F/K/R)")
    parser.add_argument("to_unit", type=str, nargs="?", help="target unit (C/F/K/R)")
    parser.add_argument("-p", "--precision", type=int, default=2, help="decimal places")
    parser.add_argument("--list", action="store_true", help="show example conversions")
    args = parser.parse_args()

    if args.list:
        print(list_examples())
        return

    # If no positional args → interactive
    if args.value is None or args.from_unit is None or args.to_unit is None:
        interactive(args.precision)
        return

    try:
        out = convert(args.value, args.from_unit, args.to_unit)
        src = format_out(args.value, canonicalize_unit(args.from_unit), args.precision)
        dst = format_out(out, canonicalize_unit(args.to_unit), args.precision)
        print(f"{src} = {dst}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def interactive(default_precision: int = 2):
    print("Unified Temperature Converter (C, F, K, R)")
    print("Type 'q' at any prompt to quit. Press Enter to keep defaults.\n")
    precision = default_precision

    while True:
        s_val = input("Enter value (e.g. 25): ").strip()
        if s_val.lower() == "q":
            break
        if not s_val:
            print("Please enter a number.")
            continue
        try:
            value = float(s_val)
        except ValueError:
            print("That wasn't a valid number. Try again.")
            continue

        f_unit = input("From unit [C/F/K/R or words like 'celsius'] : ").strip()
        if f_unit.lower() == "q":
            break
        t_unit = input("To unit [C/F/K/R] : ").strip()
        if t_unit.lower() == "q":
            break

        p_in = input(f"Precision (current {precision}) : ").strip()
        if p_in.lower() == "q":
            break
        if p_in:
            try:
                precision = max(0, int(p_in))
            except ValueError:
                print("Precision must be an integer; keeping previous value.")

        try:
            out = convert(value, f_unit, t_unit)
            src = format_out(value, canonicalize_unit(f_unit), precision)
            dst = format_out(out, canonicalize_unit(t_unit), precision)
            print(f"=> {src} = {dst}\n")
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    run_cli()
