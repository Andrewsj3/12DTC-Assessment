""" 06_get_price_v1: This component will ask the user for the price of a
product and check that it is valid
16/5/22
Jack Andrews
"""

import curses


def get_input(stdscr: curses.window, prompt):
    # stdscr is the terminal window on which the program is displayed
    if isinstance(prompt, tuple):
        stdscr.addstr(*prompt)
    else:
        stdscr.addstr(prompt)  # addstr prints output to the window
    string = ""
    curses.echo(True)
    # Prints the user's keystrokes as they type them
    x_pos = stdscr.getyx()[1]
    while True:
        key = stdscr.getkey()
        if (stdscr.getyx()[1] - 1) < x_pos:
            stdscr.move(stdscr.getyx()[0], x_pos)
            # Making sure that the cursor doesn't move too far back
        if key in (curses.KEY_BACKSPACE, '\b', '\x7f'):
            if len(string) > 0:
                string = string[:-1]
                stdscr.delch()  # Deletes the most recent character
            continue
        elif key in ('\r', '\n', '\r\n'):  # User has pressed enter, signalling
            break  # end of input
        else:
            string += key
    curses.echo(False)
    return string


def init_info_and_error_cols():
    # Creates the info and error colours and assigns variables to them
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    C_INFO = curses.color_pair(1)
    C_ERROR = curses.color_pair(2)
    return C_INFO, C_ERROR


def clear_line(stdscr: curses.window, *y_pos, cur_pos=None):
    # *ypos allows us to clear multiple lines in one function call
    # cur_pos allows us to control where the cursor finishes if we want that
    if cur_pos is None:
        cur_pos = stdscr.getyx()
    for pos in y_pos:
        stdscr.move(pos, 0)
        stdscr.clrtoeol()  # Clears a line
    stdscr.move(*cur_pos)  # Unpacking finish coordinates


def get_price(stdscr: curses.window):
    C_INFO, C_ERROR = init_info_and_error_cols()
    y = stdscr.getyx()[0]
    price = get_input(stdscr, (y, 0, "Enter price of product: $"))
    try:
        if not price:  # Checks if it's blank
            stdscr.addstr(y+1, 0, "Error: Price cannot be blank", C_ERROR)
            stdscr.getch()
            clear_line(stdscr, y+1, y, cur_pos=(0, 0))
            return get_price(stdscr)
        price = float(price)
        if price < 0:
            # Negative prices are invalid
            raise ValueError
        else:
            stdscr.addstr(y+1, 0, "Success", C_INFO)
            stdscr.getch()
            return price
    except ValueError:
        stdscr.addstr(y+1, 0, "Error: Price is invalid", C_ERROR)
        stdscr.getch()
        clear_line(stdscr, y+1, y, cur_pos=(0, 0))
        return get_price(stdscr)


if __name__ == "__main__":
    curses.wrapper(get_price)
