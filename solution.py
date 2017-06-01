rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [r+c for r in A for c in B]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(r, c) for r in ("ABC", "DEF", "GHI") for c in ("123", "456", "789")]

# For diagonal sudoku
diagonal_unit = [rows[i] + cols[i] for i in range(9)]
anti_diagonal_unit = [rows[i] + cols[-i-1] for i in range(9)]
diag_units = [diagonal_unit, anti_diagonal_unit]

unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[])) -  set([s])) for s in boxes)


assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    from collections import defaultdict
    naked_twins_dict = dict()
    for eachUnit in unitlist:
        same_two_digits = defaultdict(list)
        for eachBox in eachUnit:
            if len(values[eachBox]) == 2:
                same_two_digits[values[eachBox]].append(eachBox)
        for k, v in same_two_digits.items():
            if len(v) == 2:
                naked_twins_dict[(v[0], v[1])] = k
    # Eliminate the naked twins as possibilities for their peers
    for k, v in naked_twins_dict.items():
        # Set Intersection - Peers that belong to both boxes
        same_peers = peers[k[0]] & peers[k[1]]
        for eachBox in same_peers:
            values = assign_value(values, eachBox, values[eachBox].replace(v[0],""))
            values = assign_value(values, eachBox, values[eachBox].replace(v[1],""))
    return values
    



def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    If a box is already solved, remove its digit from all its peers.
    Input: The sudoku in dictionary form
    Output: Processed dictionary
    """
    boxes_one_digit = [k for k, v in values.items() if len(v) == 1]
    for eachBox in boxes_one_digit:
        for eachPeer in peers[eachBox]:
            assign_value(values, eachPeer, values[eachPeer].replace(values[eachBox], ""))
    return values

def only_choice(values):
    """
    If a digit appears only once in the unit, the corresponding box 
    can be solved instanly.
    Input: The sudoku in dictionary form
    Output: Processed dictionary
    """
    for eachUnit in unitlist:
        for eachDigit in '123456789':
            boxes_with_digit = [eachBox for eachBox in eachUnit if eachDigit in values[eachBox]]
            if len(boxes_with_digit) == 1:
                assign_value(values,boxes_with_digit[0],eachDigit)
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    # Recursively trying different assignment and apply constriant propagation
    # to solve the puzzule. Note that a shallow copy is made to the 
    # dictionary to make backtracking easier.
    # Input: The sudoku in dictionary form
    # Output: Processed dictionary
    
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes): 
        return values
    l, box = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)
    for digit in values[box]:
        newValues = values.copy()
        newValues = assign_value(newValues, box, digit)
        newValues = search(newValues)
        if newValues:
            return newValues

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))
    

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
