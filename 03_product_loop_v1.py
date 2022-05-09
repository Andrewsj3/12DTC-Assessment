"""product_loop_v1 This loop will contain the code that asks for a product name
 then the volume, then the price. Finally, it will store this data (perhaps in
 a class):
Written by Jack Andrews
6/5/22
"""
import curses


def get_input(stdscr: curses.window, prompt):
    # stdscr is the terminal window on which the program is displayed
    stdscr.addstr(prompt)  # addstr prints output to the window
    string = ""
    curses.echo(True)  # Prints the user's keystrokes as they type them
    while True:
        key = stdscr.getkey()
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


def get_product_name(stdscr: curses.window):
    stdscr.clear()
    C_INFO, C_ERROR = init_info_and_error_cols()
    product_name = get_input(stdscr, "Enter name of product: ").title()
    if not product_name:  # If no input entered
        stdscr.addstr(1, 0, "Error: Product name cannot be blank", C_ERROR)
        stdscr.getch()
        return get_product_name(stdscr)
    else:
        for char in product_name:
            if char.isalpha():  # Checking that there is at least one
                # alphabetical character
                stdscr.addstr(1, 0, "Success", C_INFO)
                stdscr.getch()
                return product_name
        else:
            stdscr.addstr(1, 0, "Error: Product name must contain at least "
                                "one alphabetical character", C_ERROR)
            stdscr.getch()
            return get_product_name(stdscr)


def product_loop(stdscr: curses.window):
    product_name = get_product_name(stdscr)
    # Get product weight
    # Get product price
    # Store data


if __name__ == '__main__':
    curses.wrapper(product_loop)
