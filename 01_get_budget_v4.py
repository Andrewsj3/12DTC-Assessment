"""get_budget_v4 Trial 2: This version is made without the curses library to
compare and trial against v3. See Get Budget trialling for discussion of all
versions.
Written by Jack Andrews
3/5/22
"""


def get_budget():
    try:
        budget = float(input("Enter your budget: $"))
    except ValueError:
        print("Error: Please enter a valid number")
        return get_budget()
    if budget < 1:
        print("Error: Budget must be at least $1")
        return get_budget()
    return budget


if __name__ == '__main__':
    get_budget()
