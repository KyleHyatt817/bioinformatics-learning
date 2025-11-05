# Prompt user to enter temp in Kelvin
try:
    kelvin = float(input("Enter temperature in Kelvin: "))
except ValueError:
    print("n/a")  # not a number
else:
    # Absolute zero guard (Kelvin can't be below 0)
    if kelvin < 0:
        print("n/a")
    else:
        # Apply conversion formula: C = K - 273.15
        celsius = kelvin - 273.15
        # Print to two decimals
        print(f"{kelvin:.2f} K is equal to {celsius:.2f} °C")
