# TODO
from cs50 import get_string


def main():
    text = get_string("Text: ")
    grd = grade(count(text))
    if grd > 16:
        print("Grade 16+")
    elif grd < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {grd}")


def count(s):
    # Returns array counters
    # [0] .. number of sentences, [1] .. noo. words, [2] .. noo. letters
    counters = [0, 0, 0]
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # Go through text and count word etc.
    for i in range(len(s)):
        c = s[i]
        if c == "." or c == "!" or c == "?":
            counters[0] += 1
        elif c == " ":
            counters[1] += 1
        elif c in alphabet:
            counters[2] += 1

    # Increase noo. words by one (spaces are counted)
    if len(s) > 0:
        counters[1] += 1

    return counters


def grade(arr):
    # Use Foleman-Liau formula, return the Grade
    L = arr[2] / arr[1] * 100
    S = arr[0] / arr[1] * 100
    index = 0.0588 * L - 0.296 * S - 15.8
    return round(index)


if __name__ == "__main__":
    main()