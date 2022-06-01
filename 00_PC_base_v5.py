"""PC_base_v5: Now includes post-usability testing changes: Asks for weight/
volume of product depending on base unit, updated display so "Unit Price"
becomes "Unit Price per <base_unit>". If base unit is not kg or l, add a
multiplier so unit price is calculated per 100 g/mg/ml. Final Version
(probably)
Jack Andrews
30/5/22
"""

# global imports
import curses
import re

# Common curses functions:
# stdscr.addstr() - print
# stdscr.getyx() - gets current co-ordinates of cursor
# stdscr.getch() - waits for key press
# stdscr.move(y, x) - moves to new co-ordinates
# stdscr.delch() - deletes most recent character printed
# stdscr.clrtoeol() - clears a line
# stdscr.clear() - clears screen


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
    y_pos = stdscr.getyx()[0]  # If prompts are breaking, edit this line
    stdscr.move(y_pos, 0)
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


def get_budget(stdscr: curses.window):
    C_INFO, C_ERROR = init_info_and_error_cols()
    budget = get_input(stdscr, "What is your budget: $")
    try:
        budget = float(budget)

    except ValueError:
        stdscr.addstr("Error: Please enter a valid number", C_ERROR)
        y_pos = stdscr.getyx()[0]
        stdscr.getch()
        clear_line(stdscr, y_pos, y_pos-1, cur_pos=(y_pos-1, 0))
        # These three lines are to clear two previous lines and move the cursor
        # back to the start of the line
        return get_budget(stdscr)
    if budget <= 0:
        stdscr.addstr("Error: Budget must be more than $0", C_ERROR)
        y_pos = stdscr.getyx()[0]
        stdscr.getch()
        clear_line(stdscr, y_pos, y_pos - 1, cur_pos=(y_pos-1, 0))
        return get_budget(stdscr)
    return budget


def get_unit(stdscr: curses.window):
    multiplier = 1
    C_INFO, C_ERROR = init_info_and_error_cols()
    stdscr.clear()
    unit = get_input(stdscr, "Enter base unit: ").lower()
    solid_measures = ['mg', 'g', 'kg']
    # We want to be able to differentiate between these two later
    liquid_measures = ['ml', 'l']
    if unit in solid_measures or unit in liquid_measures:
        if unit in ('g', 'ml'):
            multiplier = 100
        elif unit == 'mg':
            multiplier = 1000
        # These changes were made because previously, if you selected grams as
        # the base unit, it would calculate the unit price as cost per g.
        # However, with the multiplier, this has been changed to cost per 100g
        # which makes it far more useful

        if multiplier != 1:
            stdscr.addstr("Unit price is now calculated at cost per"
                          f" {multiplier}{unit}\n", C_INFO)
        else:
            stdscr.addstr("Unit price is now calculated at cost per"
                          f" {unit}\n", C_INFO)
        return unit, multiplier
    else:
        stdscr.addstr("Error: Please enter a valid unit", C_ERROR)
        y_pos = stdscr.getyx()[0]
        stdscr.getch()
        clear_line(stdscr, y_pos, y_pos - 1, cur_pos=(y_pos - 1, 0))
        return get_unit(stdscr)


def get_product_name(stdscr: curses.window):
    C_INFO, C_ERROR = init_info_and_error_cols()
    product_name = get_input(stdscr, "Enter name of product: ").title()
    if not product_name:  # If no input entered
        stdscr.addstr("Error: Product name cannot be blank", C_ERROR)
        y_pos = stdscr.getyx()[0]
        stdscr.getch()
        clear_line(stdscr, y_pos, y_pos - 1, cur_pos=(y_pos-1, 0))
        return get_product_name(stdscr)
    else:

        for char in product_name:
            if char.isalpha():  # Checking that there is at least one
                # alphabetical character
                return product_name
        else:
            stdscr.addstr("Error: Product name must contain at least "
                          "one alphabetical character", C_ERROR)
            y_pos = stdscr.getyx()[0]
            stdscr.getch()
            clear_line(stdscr, y_pos, y_pos-1, cur_pos=(y_pos-1, 0))
            return get_product_name(stdscr)


def get_price(stdscr: curses.window):
    C_INFO, C_ERROR = init_info_and_error_cols()
    price = get_input(stdscr, "Enter price of product: $")

    try:
        if not price:  # Checks if it's blank
            stdscr.addstr("Error: Price cannot be blank", C_ERROR)
            y_pos = stdscr.getyx()[0]
            stdscr.getch()
            clear_line(stdscr, y_pos, y_pos-1, cur_pos=(y_pos-1, 0))
            return get_price(stdscr)
        price = float(price)
        if price < 0:
            # Negative prices are invalid
            raise ValueError
        else:
            return price

    except ValueError:
        stdscr.addstr("Error: Price is invalid", C_ERROR)
        y_pos = stdscr.getyx()[0]
        stdscr.getch()
        clear_line(stdscr, y_pos, y_pos-1, cur_pos=(y_pos-1, 0))
        return get_price(stdscr)


def parse_volume(stdscr: curses.window, base_unit):
    C_INFO, C_ERROR = init_info_and_error_cols()
    solid_units = ["mg", 'g', "kg"]
    liquid_units = ["ml", 'l']
    if base_unit in solid_units:
        valid_units = solid_units
        prompt = f"Enter weight of product in the form '1{base_unit}': "
    else:
        valid_units = liquid_units
        prompt = f"Enter volume of product in the form '1{base_unit}': "

    info = get_input(stdscr, prompt).lower()
    info = info.strip().replace(" ", "")  # Removing all spaces from user input
    num_pattern = re.compile(r"^[0-9]+(\.[0-9]+)?")
    # This pattern matches at least one number, possibly followed by a decimal
    # and at least another number to get the weight component of the product
    idx = 0

    if re.fullmatch(r"^[0-9]+(\.[0-9]+)?[a-z]+$", info):
        # Ensuring user enters valid input
        matches = num_pattern.finditer(info)
        for match in matches:
            idx = match.end()  # Index of last digit in input

        weight = float(info[:idx])
        if not (weight > 0):
            stdscr.addstr("Error: Product weight must be more than 0", C_ERROR)
            y_pos = stdscr.getyx()[0]
            stdscr.getch()
            clear_line(stdscr, y_pos, y_pos-1, cur_pos=(y_pos-1, 0))
            return parse_volume(stdscr, base_unit)

        unit = info[idx:]  # Splitting the strings into the two components
        if unit not in valid_units:
            stdscr.addstr(
                f"Error: {unit} is either invalid or cannot be converted into"
                f" {base_unit}", C_ERROR)
            y_pos = stdscr.getyx()[0]
            stdscr.getch()
            clear_line(stdscr, y_pos, y_pos-1, cur_pos=(y_pos-1, 0))
            return parse_volume(stdscr, base_unit)
        return weight, unit

    else:
        stdscr.addstr("Error: Input was not in expected format", C_ERROR)
        y_pos = stdscr.getyx()[0]
        stdscr.getch()
        clear_line(stdscr, y_pos, y_pos-1, cur_pos=(y_pos-1, 0))
        # Doing some fancy unpacking to clear multiple lines at once
        return parse_volume(stdscr, base_unit)


def conv_to_base(unit, price, weight, base_unit, multiplier):
    solid_units = ["mg", 'g', "kg"]
    liquid_units = ["ml", 'l']
    if base_unit in solid_units:
        diff = solid_units.index(base_unit) - solid_units.index(unit)
    else:
        diff = liquid_units.index(base_unit) - liquid_units.index(unit)
        # This below statement converts the price with respect to weight into
        # the price of a base unit * a multiplier if there is one.
        # e.g. product weighing 200 grams costing $2 = $10/kg
    return round(price * (multiplier * (1000 ** diff) / weight), 2)


def list_data(stdscr: curses.window, product_list, budget, qty, base_unit):
    init_info_and_error_cols()
    stdscr.clear()
    product_list.sort(key=lambda x: len(x['name']), reverse=True)
    # Longest names first, shortest names last
    longest_name = len(product_list[0]['name'])

    for name in product_list:
        name['name'] = name['name'].ljust(longest_name)
    stdscr.addstr(f"{'Name'.ljust(longest_name)}\t|Weight |Unit   |Price"
                  f"  |Unit Price per {qty if qty != 1 else ''}{base_unit}\n")

    # Using ljust to make sure that everything is aligned
    # This method is much better and more reliable than the previous one
    product_list.sort(key=lambda y: y['unit_price'])
    # Sorting by cheapest unit price first

    for item in product_list:
        name, weight, unit, price, unit_price = item.values()
        col = ((budget >= price) ^ 1) + 1  # Evil bit manipulation to select
        # the colour
        # Step 1: compare whether budget is greater than price. If so, the
        # variable has a numeric value of 1, else 0.
        # Step 2: Apply exclusive or. This returns true if ONLY one condition
        # is true, so 1^1 = False, 0^1 = True
        # Step 3: Add one so our variable can be either 1 or 2, which is the id
        # of our colours.
        # Equivalent to:
        # if budget >= price:
        #   col = 1
        # else:
        #   col = 2
        stdscr.addstr(f"{name}\t|{weight}\t|{unit}\t|${price:.2f}\t|"
                      f"${unit_price:.2f}\t\n", curses.color_pair(col))
        # Formatting all the headings


def yes_no(stdscr: curses.window, prompt):
    C_INFO, C_ERROR = init_info_and_error_cols()
    response = get_input(stdscr, prompt).lower()
    if response in ("y", "yes"):
        return True
    elif response in ("n", "no"):
        stdscr.clear()
        return False

    elif response == '':  # blank
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


def best_item(stdscr: curses.window, budget, product_list):
    C_INFO, _ = init_info_and_error_cols()
    product_list.sort(key=lambda item: item['unit_price'])
    # Cheapest items first
    for thing in product_list:
        thing["name"] = thing.get("name").rstrip()
        # When the table was being formatted, the names would have spaces at
        # the end of them, hence the need for rstrip
        if thing.get("price") <= budget:
            # Note that even if an item is cheaper for value, it won't be
            # recommended if it is out of budget
            stdscr.addstr(f"{thing['name']} is the cheapest option\n")
            stdscr.addstr("Press any key to exit...")
            stdscr.getch()
            return

    else:
        stdscr.addstr(f"No items fit your budget, but "
                      f"{product_list[0].get('name')} is the cheapest option "
                      f"for value\n")
        stdscr.addstr("Press any key to exit...")
        stdscr.getch()
        # The item at product_list[0] will be the cheapest for value because it
        # has been sorted that way


def product_loop(stdscr: curses.window, base_unit, budget, multiplier):
    product_list = []
    products_compared = 0
    while True:
        product_name = get_product_name(stdscr)
        p_weight, p_unit = parse_volume(stdscr, base_unit)
        product_price = get_price(stdscr)
        product_data = {'name': product_name, 'weight': p_weight,
                        'unit': p_unit,
                        'price': product_price,
                        'unit_price': conv_to_base(p_unit, product_price,
                                                   p_weight, base_unit,
                                                   multiplier)}
        product_list.append(product_data)

        y_pos = stdscr.getyx()[0]
        clear_line(stdscr, *[i for i in range(y_pos, 0, -1)], cur_pos=(1, 0))
        # Clears the old prompts off the screen
        products_compared += 1
        if products_compared >= 2:  # Doesn't make sense to ask the question
            # if user has only entered info for one product
            if yes_no(stdscr, "Do you want to compare "
                              "another product (y/n): "):
                continue
            else:
                stdscr.addstr("Press any key to display the table. Items "
                              "that fit in the budget are green, those that "
                              "don't are red.")
                stdscr.getch()
                list_data(stdscr, product_list, budget, multiplier, base_unit)
                return product_list


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


# Main routine begins
def main(stdscr: curses.window):
    while True:
        max_y, _ = stdscr.getmaxyx()
        # Finding the height of the terminal
        if max_y < 14:  # Just enough lines to display instructions
            stdscr.clear()
            stdscr.addstr("Terminal height is too low. Increase terminal"
                          " height until message disappears")
            # If it is too low, messages may overlap and the program will not
            # work properly
            stdscr.getch()
        else:
            stdscr.clear()
            break
    instructions(stdscr)
    budget = get_budget(stdscr)
    base_unit, multiplier = get_unit(stdscr)
    product_list = product_loop(stdscr, base_unit, budget, multiplier)
    best_item(stdscr, budget, product_list)


if __name__ == "__main__":
    curses.wrapper(main)
