"""10_instructions_v1: This function asks the user if they want to see the
instructions. If they say yes, the instructions show, and the program starts.
Otherwise, instructions are skipped.
Jack Andrews
1/06/22
"""

import curses


def init_info_and_error_cols():
    # Creates the info and error colours and assigns variables to them
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    C_INFO = curses.color_pair(1)
    C_ERROR = curses.color_pair(2)
    return C_INFO, C_ERROR


def yes_no(stdscr: curses.window, prompt):
    C_INFO, C_ERROR = init_info_and_error_cols()
    response = get_input(stdscr, prompt).lower()
    if response in ("y", "yes"):
        return True
    elif response in ("n", "no"):
        stdscr.clear()
        return False

    elif response == '':
        stdscr.addstr("Error: Response cannot be blank", C_ERROR)
        y_pos = stdscr.getyx()[0]
        stdscr.getch()
        clear_line(stdscr, y_pos, y_pos-1, cur_pos=(y_pos-1, 0))
        return yes_no(stdscr, prompt)

    else:
        stdscr.addstr("Error: Response must be either 'y', 'yes',"
                      " or 'n', 'no'", C_ERROR)
        y_pos = stdscr.getyx()[0]
        stdscr.getch()
        clear_line(stdscr, y_pos, y_pos-1, cur_pos=(y_pos-1, 0))
        return yes_no(stdscr, prompt)


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
    y_pos = stdscr.getyx()[0]
    stdscr.move(y_pos, 0)
    return string


def clear_line(stdscr: curses.window, *y_pos, cur_pos=None):
    # *ypos allows us to clear multiple lines in one function call
    # cur_pos allows us to control where the cursor finishes if we want that
    if cur_pos is None:
        cur_pos = stdscr.getyx()
    for pos in y_pos:
        stdscr.move(pos, 0)
        stdscr.clrtoeol()  # Clears a line
    stdscr.move(*cur_pos)  # Unpacking finish coordinates


def instructions(stdscr: curses.window):
    # This function displays the instructions if the user wishes
    C_INFO, _ = init_info_and_error_cols()
    if yes_no(stdscr, "Do you want to see the instructions (y/n): "):
        stdscr.clear()
        stdscr.addstr("***** Instructions *****:\n", C_INFO)
        stdscr.addstr("Welcome to the Price Comparison Tool!\n"
                      "This tool can be used to compare similar products.\n"
                      "Start by entering your budget, then the base unit.\n"
                      "This will be used to calculate the unit price of each\n"
                      "product, i.e. a product weighing 500g which costs $1\n"
                      "has a unit price of $2/kg. For each product you want\n"
                      "to compare, you will need to enter its name, then the\n"
                      "weight/volume depending on the product, and finally,\n"
                      "its price. When you are done, a table will be\n"
                      "displayed showing all the info, and the program will\n"
                      "tell you which item is best for you.\n")
        stdscr.addstr("Press any key to start", C_INFO)
    else:
        stdscr.addstr("Press any key to start", C_INFO)
    stdscr.getch()
    stdscr.clear()


if __name__ == '__main__':
    curses.wrapper(instructions)
