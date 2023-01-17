# TODO
from cs50 import get_int

# Get input
while(True):
    height = get_int("Height: ")
    if height >= 1 and height <= 8:
        break

# Print stairs
counter = 1
for i in range(height):
    print(" " * (height - counter), end="")
    print("#" * counter, end="")
    print("  ", end="")
    print("#" * counter, end="")
    print("\n", end="")
    counter += 1