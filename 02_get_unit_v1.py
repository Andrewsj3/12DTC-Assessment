import curses


# Reusing get_input from previous component
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


def get_unit(stdscr: curses.window):
    C_INFO, C_ERROR = init_info_and_error_cols()
    stdscr.clear()
    unit = get_input(stdscr, "Enter base unit: ").lower()
    solid_measures = ['mg', 'g', 'kg']
    # We want to be able to differentiate between these two later
    liquid_measures = ['ml', 'l']
    if unit in solid_measures or unit in liquid_measures:
        stdscr.addstr(1, 0, "Success", C_INFO)
        stdscr.getch()
        return unit
    else:
        stdscr.addstr(1, 0, "Error: Please enter a valid unit", C_ERROR)
        stdscr.getch()
        return get_unit(stdscr)


if __name__ == '__main__':
    curses.wrapper(get_unit)
