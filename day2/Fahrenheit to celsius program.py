#promt user to enter temp in Celcis
celsius = float(input("Enter temperture in Celsius"))
#apply conversion formula
fahrenheit = (celsius * 9/5) + 32
#display the coverted temp in Fahrenheig formatted to two deci.
print(f"{celsius:.2f} °C is equal to {fahrenheit:.2f} °F")
