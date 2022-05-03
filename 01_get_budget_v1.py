"""get_budget_v1 Trial 1: This function takes input from the user and checks
that it is a valid integer or float. This trial uses the curses library to add
colour to text for better aesthetics.
Written by Jack Andrews
2/5/22
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


def get_budget(stdscr: curses.window):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    C_INFO = curses.color_pair(1)
    C_ERROR = curses.color_pair(2)
    decimals = 0
    budget = get_input(stdscr, "What is your budget: $")
    for char in budget:
        if not char.isdigit():
            if char == '.':
                decimals += 1
            else:
                stdscr.addstr("\nError:"
                              " Please enter a valid number\n", C_ERROR)
                stdscr.addstr("\nPress any key to continue...", C_INFO)
                stdscr.refresh()
                stdscr.getch()
                stdscr.clear()
                return get_budget(stdscr)
    if decimals > 1:
        stdscr.addstr("\nError: Please enter a valid number\n", C_ERROR)
        stdscr.addstr("\nPress any key to continue...", C_INFO)
        stdscr.refresh()
        stdscr.getch()
        stdscr.clear()
        return get_budget(stdscr)
    if float(budget) < 1:
        stdscr.addstr("\nError: Budget must be at least $1\n", C_ERROR)
        stdscr.addstr("\nPress any key to continue...", C_INFO)
        stdscr.refresh()
        stdscr.getch()
        stdscr.clear()
        return get_budget(stdscr)
    stdscr.addstr("\nSuccess", C_INFO)
    stdscr.getch()
    return budget


if __name__ == '__main__':
    curses.wrapper(get_budget)
