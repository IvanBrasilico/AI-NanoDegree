rows = 'ABCDEFGHI'
cols = '123456789'
DIGITS = '123456789'


def cross(a, b):
    return [s + t for s in a for t in b]


boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI')
                for cs in ('123', '456', '789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    return


def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    assert(len(grid) == 81)
    result = dict()
    for key, value in zip(boxes, grid):
        if value == '.':
            value = DIGITS
        result[key] = value
    return result


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    for key, value in values.items():
        if len(value) == 1:  # Unique value for this box (box solved)
            box_peers_keys = peers[key]
            for peer_key in box_peers_keys:
                peer_value = values[peer_key]
                if len(peer_value) > 1:
                    peer_value = peer_value.replace(value, '')
                    values[peer_key] = peer_value
    return values
 

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for digit in DIGITS:
            digit_count = 0
            target_box = ''
            for box in unit:
                if digit in values[box]:
                    digit_count += 1
                    if digit_count == 1:
                        target_box = box
            if digit_count == 1:
                values[target_box] = digit
    return values


def solved(values):
    """
    Check if Sudoku is solved. In fact, just check if all cells have only one digit.
    Otherwise The first cell with more than one digit or not a digit will be returned.
    """
    for key, value in values.items():
        if len(value) > 1:
            return key
        if value not in DIGITS:
            return key
    return True


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len(
            [box for box in values.keys() if len(values[box]) == 1])
        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len(
            [box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = ((solved_values_after == 81) or
                   (solved_values_before == solved_values_after))
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False
    # Choose one of the unfilled squares with the fewest possibilities
    not_solved = {key: value for key,
                  value in values.items() if len(value) > 1}
    if len(not_solved) == 0:
        return values
    sorted_keys = [key for key, value in sorted(not_solved.items(),
                                                    key=lambda x: len(x[1]))]
    key = sorted_keys[0]
    box = values[key]
    for digit in box:
        new_sudoku = values.copy()
        new_sudoku[key] = digit
        attempt = search(new_sudoku)
        if attempt:
            return attempt

sudokus = ('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..',
           '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......')

for sudoku in sudokus:
    values = grid_values(sudoku)
    display(values)
    print('.......')
    values = search(values)
    display(values)


def solve_by_reps(values, max_reps=5):
    while solved(values) is not True:
        cont = 1
        values = eliminate(values)
        display(values)
        print('.......')
        values = only_choice(values)
        display(values)
        print('..... After ', cont, ' iterations...')
        cont += 1
        if cont > max_reps:
            print('Não pude resolver sudoku')
            break
