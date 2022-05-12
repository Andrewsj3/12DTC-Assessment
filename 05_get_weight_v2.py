"""get_weight_v2: This function asks user for a unit and a weight and checks
that they are valid. Now checks units to see if they can be compared with each
other.
Written by Jack Andrews
10/5/22
"""

import curses


def get_input(stdscr: curses.window, prompt):
    # stdscr is the terminal window on which the program is displayed
    if isinstance(prompt, tuple):
        stdscr.addstr(*prompt)
    else:
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
    unit = get_input(stdscr, (1, 0, "Enter unit: ")).lower()
    solid_measures = ['mg', 'g', 'kg']
    # We want to be able to differentiate between these two later
    liquid_measures = ['ml', 'l']
    if unit in solid_measures:
        return unit
    elif unit in liquid_measures:
        return unit
    else:
        y_pos = stdscr.getyx()[0]  # Keeping track of coordinates
        stdscr.addstr(y_pos + 1, 0,
                      "Error: Please enter a valid unit", C_ERROR)
        stdscr.getch()
        clear_line(stdscr, 2, 1)
        return get_unit(stdscr)


def clear_line(stdscr: curses.window, *y_pos, cur_pos=0):
    # *ypos allows us to clear multiple lines in one function call
    # cur_pos allows us to control where the cursor finishes if we want that
    if cur_pos == 0:
        cur_pos = stdscr.getyx()
    for pos in y_pos:
        stdscr.move(pos, 0)
        stdscr.clrtoeol()  # Clears a line
    stdscr.move(*cur_pos)  # Unpacking finish coordinates


def get_weight(stdscr: curses.window):
    C_INFO, C_ERROR = init_info_and_error_cols()
    unit = get_unit(stdscr)
    while True:
        y_pos = stdscr.getyx()[0]
        stdscr.move(y_pos+1, 0)
        try:
            weight = get_input(stdscr, (2, 0, "Enter weight: "))
            # get_input has been updated to allow us to send the co-ordinates
            # of the prompt and a color if we wish
            weight = float(weight)
            if weight < 0:
                raise ValueError
            return unit, weight
        except ValueError:
            y_pos = stdscr.getyx()[0]
            stdscr.addstr(y_pos+1, 0, "Error: Please enter a valid weight",
                          C_ERROR)
            stdscr.getch()
            clear_line(stdscr, y_pos+1, y_pos)
            continue


def main(stdscr: curses.window):
    solid_measures = ['mg', 'g', 'kg']
    liquid_measures = ['ml', 'l']
    C_INFO, C_ERROR = init_info_and_error_cols()
    base_unit = get_input(stdscr, "Enter base unit for testing: ")
    if base_unit in solid_measures:
        valid_units = solid_measures.copy()
    else:
        valid_units = liquid_measures.copy()
    unit, weight = get_weight(stdscr)
    while True:
        if unit not in valid_units:
            stdscr.addstr(3, 0, f"Error: {unit} are incompatible with"
                                f" {base_unit}", C_ERROR)
            stdscr.getch()
            y_pos = stdscr.getyx()[0]
            clear_line(stdscr, y_pos, y_pos - 1, y_pos - 2)
            unit, weight = get_weight(stdscr)
        break
    stdscr.addstr(3, 0, "Success", C_INFO)
    stdscr.getch()


if __name__ == '__main__':
    curses.wrapper(main)
