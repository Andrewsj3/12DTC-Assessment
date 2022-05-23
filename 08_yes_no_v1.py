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
    y_pos = stdscr.getyx()[0] + 1
    stdscr.move(y_pos, 0)  # Moving cursor to next line automatically to make
    # life easier
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


def yes_no(stdscr: curses.window, prompt):
    C_INFO, C_ERROR = init_info_and_error_cols()
    start_pos = stdscr.getyx()[0]
    # Getting the start position, so we can return to it later
    response = get_input(stdscr, prompt).lower()
    if response in ("y", "yes"):
        stdscr.addstr("You want to compare another product", C_INFO)
        stdscr.getch()
        return response
    elif response in ("n", "no"):
        stdscr.addstr("You do not want to compare another product", C_INFO)
        stdscr.getch()
        return response
    elif response == '':
        stdscr.addstr("Error: Response cannot be blank", C_ERROR)
        y_pos = stdscr.getyx()[0]
        stdscr.getch()
        clear_line(stdscr, *[i for i in range(y_pos, start_pos-1, -1)],
                   cur_pos=(0, 0))
        return yes_no(stdscr, prompt)
    else:
        stdscr.addstr("Error: Response must be either 'y', 'yes',"
                      " or 'n', 'no'", C_ERROR)
        y_pos = stdscr.getyx()[0]
        stdscr.getch()
        clear_line(stdscr, *[i for i in range(y_pos, start_pos-1, -1)],
                   cur_pos=(0, 0))
        return yes_no(stdscr, prompt)


if __name__ == '__main__':
    curses.wrapper(yes_no, "Do you want to compare another product? ")
