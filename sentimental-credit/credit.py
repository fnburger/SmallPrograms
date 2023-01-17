# TODO
from cs50 import get_int
import sys

# Get input
nmb = get_int("Number: ")
# Exit if input is not a sequence of digits with the right length
if nmb < pow(10, 12) or nmb > 9999999999999999:
    print("INVALID\n")
    sys.exit(1)

# Luhn's algorithm (is pot. cc nmbr?)
n = nmb
sum = 0
flip = False

while n > 0:
    dgt = int(n % 10)
    if flip:
        dgt = dgt * 2
    if dgt > 9:
        sum = sum + (dgt - 9)
    else:
        sum = sum + dgt
    n = int(n / 10)
    flip = not flip

# Determine card provider
type = "INVALID"
if (sum % 10) == int(0):
    if (nmb // pow(10, 13)) == 34 or (nmb // pow(10, 13)) == 37:
        type = "AMEX"
    if (nmb // pow(10, 14)) >= 51 and (nmb // pow(10, 14)) <= 55:
        type = "MASTERCARD"
    if (nmb // pow(10, 15)) == 4 or (nmb // pow(10, 12)) == 4:
        type = "VISA"

# Print result
print(f"{type}\n")
sys.exit(0)