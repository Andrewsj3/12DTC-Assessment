"""get_budget_v2 Trial 1: Introduced new function to print errors, making code
more efficient, as well as one to initialize the info and error colours used.
This trial uses the curses library to add colour to text for better aesthetics.
Written by Jack Andrews
3/5/22
"""
import curses


def get_input(stdscr: curses.window, prompt):
    stdscr.addstr(prompt)
    stdscr.refresh()
    string = ""
    while True:
        key = stdscr.getkey()
        if key != '\n':
            string += key
            stdscr.addstr(key)
            stdscr.refresh()
        else:
            break
    return string


def print_err(stdscr: curses.window, prompt):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    C_INFO = curses.color_pair(1)
    C_ERROR = curses.color_pair(2)
    stdscr.addstr(f"\n{prompt}\n", C_ERROR)
    stdscr.addstr("\nPress any key to continue...", C_INFO)
    stdscr.refresh()
    stdscr.getch()
    stdscr.clear()


def init_info_and_error_cols():
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    C_INFO = curses.color_pair(1)
    C_ERROR = curses.color_pair(2)
    return C_INFO, C_ERROR


def get_budget(stdscr: curses.window):
    C_INFO, C_ERROR = init_info_and_error_cols()
    decimals = 0
    budget = get_input(stdscr, "What is your budget: $")
    for char in budget:
        if not char.isdigit():
            if char == '.':
                decimals += 1
            else:
                print_err(stdscr, "Error: Please enter a valid number")
                return get_budget(stdscr)
    if decimals > 1:
        print_err(stdscr, "Error: Please enter a valid number")
        return get_budget(stdscr)
    if float(budget) < 1:
        print_err(stdscr, "Error: Budget must be at least $1")
        return get_budget(stdscr)
    stdscr.addstr("\nSuccess", C_INFO)
    stdscr.getch()
    return budget


if __name__ == '__main__':
    curses.wrapper(get_budget)
