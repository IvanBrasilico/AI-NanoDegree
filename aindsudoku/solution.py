
from utils import *

DIGITS = '123456789'

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI')
                for cs in ('123', '456', '789')]
diagonal_units = [r + c for r, c in zip(rows, cols)]
diagonal_units_2 = [r + c for r, c in zip(rows, cols[::-1])]
diagonal_units = [diagonal_units] + [diagonal_units_2]

unitlist = row_units + column_units + square_units + diagonal_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    twinslist = []
    for unit in unitlist:  # Process each "unit" (rows, cols, 3x3, diags)
        unit_boxes = set()
        twins = set()
        for box_key in unit:  # Look for twins on unit
            abox = values[box_key]
            if len(abox) == 2:
                if abox in unit_boxes:
                    twins.add(abox)
                unit_boxes.add(abox)
        twinslist.append(twins)
    print(twinslist)
    for unit, twins in zip(unitlist, twinslist):
        if twins:
            print('Found pairs ', twins, ' - Unit: ', unit)
            for peer_key in unit:  # Eliminate twin number from Unit if exists
                peer_value = values[peer_key]
                for twin in twins:
                    if twin != peer_value:  # Do not eliminate self
                            # (len(twin) < len(peer_value))):  # or smaller value
                        for digit in twin:
                            peer_value = peer_value.replace(digit, '')
                values[peer_key] = peer_value
    return values


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    for key, value in values.items():
        if len(value) == 1: # box solved
            box_peers_keys = peers[key]
            for peer_key in box_peers_keys:
                peer_value = values[peer_key]
                peer_value = peer_value.replace(value, '')
                values[peer_key] = peer_value
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
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


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len(
            [box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Use the Naked Twins Strategy
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len(
            [box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = (solved_values_before == solved_values_after)
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
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


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.

        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grids = (
        '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3',
        '........4......1.....6......7....2.8...372.4.......3.7......4......5.6....4....2.',
        '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    )
    cont = 0
    for diag_sudoku_grid in diag_sudoku_grids:
        display(grid2values(diag_sudoku_grid))
        result = solve(diag_sudoku_grid)
        print('....')
        # print(result)
        display(result)
        cont += 1
        print(cont)

    print('Other')
    other_grid = {"B6": "236789", "F1": "1", "G8": "345678", "H8": "345678", "F2": "24", "I2": "2345678", "C7": "2345678", "A9": "2458", "B4": "345678", "I7": "1", "B3": "1234569", "H6": "1236789", "B2": "1234568", "D8": "2", "G5": "23456789", "D4": "1", "A8": "345689", "D6": "5", "F7": "58", "H2": "12345678", "B5": "23456789", "H1": "23456789", "G2": "12345678", "F3": "24", "H3": "1234569", "A2": "234568", "H4": "345678", "C3": "1234569", "C1": "2345689","E1": "567", "D5": "36", "E4": "2", "C9": "124578", "E9": "3", "D3": "8", "A5": "1", "F6": "37", "F5": "37", "D7": "47", "C8": "3456789", "B9": "124578", "B7": "2345678", "H7": "2345678", "F8": "58", "C2": "1234568", "D2": "9", "G6": "1236789", "A7": "234568", "E5": "678", "C6": "236789", "H9":"24578", "C4": "345678", "E8": "1", "E3": "56", "I1": "2345678", "A4": "34568", "F4": "9", "I4": "345678", "A3": "7", "B8": "3456789", "I6": "23678", "F9": "6", "D1": "36", "B1": "2345689", "C5": "23456789", "I5": "2345678", "I3": "23456", "G1": "23456789", "I9": "9", "A1": "2345689", "E7": "9", "I8": "345678", "D9": "47", "G4": "345678", "E2": "567", "G9": "24578", "G3": "1234569", "G7": "2345678", "H5": "23456789", "E6": "4", "A6": "23689"}
    display(other_grid)
    result = naked_twins(other_grid)
    # print(result)
    display(result)
    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
