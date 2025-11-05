def convert_temp(value, from_unit, to_unit):
    """
    Convert temperature between Celsius (C), Fahrenheit (F), and Kelvin (K).
    Returns a float.
    """
    u_from = str(from_unit).strip().upper()
    u_to   = str(to_unit).strip().upper()

    allowed = {"C", "F", "K"}
    if u_from not in allowed or u_to not in allowed:
        raise ValueError("Units must be 'C', 'F', or 'K'")

    # If units match, nothing to do.
    if u_from == u_to:
        return float(value)

    # Convert input to Celsius
    x = float(value)
    if u_from == "C":
        c = x
    elif u_from == "F":
        c = (x - 32.0) * 5.0 / 9.0
    else:  # "K"
        c = x - 273.15

    # Absolute zero guard (allow a hair of float noise)
    if c < -273.15 - 1e-9:
        raise ValueError("Temperature below absolute zero.")

    # Convert from Celsius to target
    if u_to == "C":
        result = c
    elif u_to == "F":
        result = c * 9.0 / 5.0 + 32.0
    else:  # "K"
        result = c + 273.15

    return float(result)


# ---- quick self-tests (run only when this file is executed) ----
if __name__ == "__main__":
    print(convert_temp(0, "C", "F"))      # expect 32.0
    print(convert_temp(32, "F", "C"))     # expect 0.0
    print(convert_temp(300, "K", "F"))    # ~80.33

    try:
        print(convert_temp(-1, "K", "C"))  # should raise
    except ValueError as e:
        print("caught:", e)