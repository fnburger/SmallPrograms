import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py database.csv dna.txt")
        sys.exit(1)

    # TODO: Read database file into a variable
    db = []
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        for row in reader:
            db.append(dict(row))
        fields = list(reader.fieldnames)

    # TODO: Read DNA sequence file into a variable
    f = open(sys.argv[2], 'r')
    dna = f.read()

    # TODO: Find longest match of each STR in DNA sequence

    # Look at every field except "name"
    # and compute longest run of consecutive
    # repeats of that STR in the DNA
    longest_runs = []
    # For every STR...
    for fieldname in fields[1:]:
        # ...save the length of the longest run
        longest_runs.append(longest_match(dna, fieldname))

    # TODO: Check database for matching profiles
    found_match = False
    for entry in db:
        matching = 0
        count = 0
        for fld in entry:
            # Don't count the name field...
            # ...(longest_runs has no elements corresponding to it)
            if fld == "name":
                continue
            if int(entry[fld]) == int(longest_runs[count]):
                matching += 1
            count += 1
        if matching == len(fields)-1:
            print(entry["name"])
            found_match = True

    if not found_match:
        print("No match")

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()