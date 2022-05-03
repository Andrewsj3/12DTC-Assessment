"""PC_base_v1: Integrate get_budget into the main program and import the curses
library. get_budget takes input from the user and makes sure it is a float.
Jack Andrews
3/5/22
"""

# global imports
import curses

# functions


def get_input(stdscr: curses.window, prompt):
    # stdscr is the terminal window on which the program is displayed
    curses.echo()
    stdscr.addstr(prompt)  # addstr prints output to the window
    stdscr.refresh()  # updates the screen
    string = stdscr.getstr()
    return string


def print_err(stdscr: curses.window, prompt):
    # Initializing colours
    C_INFO, C_ERROR = init_info_and_error_cols()
    stdscr.addstr(f"\n{prompt}\n", C_ERROR)
    stdscr.addstr("\nPress any key to continue...", C_INFO)
    stdscr.refresh()
    stdscr.getch()  # Waits for user to press a key,
    stdscr.clear()  # then clears the screen


def init_info_and_error_cols():
    # Creates the info and error colours and assigns variables to them
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    C_INFO = curses.color_pair(1)
    C_ERROR = curses.color_pair(2)
    return C_INFO, C_ERROR


def get_budget(stdscr: curses.window):
    budget = get_input(stdscr, "What is your budget: $")
    try:
        budget = float(budget)
    except ValueError:
        print_err(stdscr, "\nError: Please enter a valid number")
        return get_budget(stdscr)
    if budget < 1:
        print_err(stdscr, "\nError: Budget must be at least $1")
        return get_budget(stdscr)
    return budget


# Main routine begins
def main(stdscr: curses.window):
    # Ask user for budget
    budget = get_budget(stdscr)
    stdscr.getch()  # Program will not close until user presses key
    # Ask for unit

    # Enter main loop

    # Ask for product name

    # Ask for product mass/volume

    # Ask for price of product

    # Calculate price per unit

    # Store details of product: name, weight, price

    # Ask user if they want to compare another product, if not, break from loop

    # Sort list by unit price

    # Show all items within budget and all items outside budget

    # Ask user if they want to compare more items, if so,
    # go to top of main routine

    # End of main routine


if __name__ == "__main__":
    curses.wrapper(main)
