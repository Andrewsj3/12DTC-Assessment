"""get_budget_v3 Trial 1: get_budget has been reworked to improve efficiency.
This trial uses the curses library to add colour to text for better aesthetics.
Written by Jack Andrews
3/5/22
"""
import curses  # Refer to docstring


def get_input(stdscr: curses.window, prompt):
    # stdscr is the terminal window on which the program is displayed
    stdscr.addstr(prompt)  # addstr prints output to the window
    stdscr.refresh()  # updates the screen
    string = ""
    while True:
        key = stdscr.getkey()
        if key != '\n':  # End input when user presses enter
            string += key
            stdscr.addstr(key)
            stdscr.refresh()
        else:
            break
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
    C_INFO, C_ERROR = init_info_and_error_cols()
    budget = get_input(stdscr, "What is your budget: $")
    try:
        budget = float(budget)
    except ValueError:
        print_err(stdscr, "\nError: Please enter a valid number")
        return get_budget(stdscr)
    if budget < 1:
        print_err(stdscr, "\nError: Budget must be at least $1")
        return get_budget(stdscr)
    stdscr.addstr("\nSuccess", C_INFO)  # for testing/debugging purposes only
    stdscr.getch()
    return budget


if __name__ == '__main__':
    curses.wrapper(get_budget)
