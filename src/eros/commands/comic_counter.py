import os
import re
from collections import Counter


def _extract_number_from_filename(filename):
    """
    Extracts the first number found in a filename.
    Returns the number as an integer, or None if no number is found.
    """
    match = re.search(r"\d+", filename)
    if match:
        return int(match.group())
    return None


def find_missing_and_duplicate_files_in_current_directory():
    """
    Finds missing and duplicate numbers in file names in the current directory.
    """
    # Get a list of all files in the current directory
    files = os.listdir(".")

    # Extract numbers from filenames
    numbers = []
    for file in files:
        number = _extract_number_from_filename(file)
        if number is not None:
            numbers.append(number)

    if numbers:
        # Count occurrences of each number
        number_counts = Counter(numbers)

        # Report duplicates
        duplicates = [num for num, count in number_counts.items() if count > 1]
        if duplicates:
            print("Duplicate numbers found:")
            for num in duplicates:
                print(f"Number {num} appears {number_counts[num]} times")
        else:
            print("No duplicate numbers found.")

        # Sort numbers and find missing numbers
        sorted_numbers = sorted(numbers)
        missing_numbers = []
        for i in range(sorted_numbers[0], sorted_numbers[-1] + 1):
            if i not in number_counts:
                missing_numbers.append(i)

        # Print missing numbers
        if missing_numbers:
            print("Missing numbers in the sequence:")
            for num in missing_numbers:
                print(f"Missing number: {num}")
        else:
            print("No missing numbers in the sequence.")
    else:
        print("No numbered files found in the current directory.")
