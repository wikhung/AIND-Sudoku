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
    n_unsolved_boxes_before = len([box for box in values if len(values[box]) > 1])
    
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    
    # Find all the boxes with only 2 digits
    dbl_digits = [box for box in values if len(values[box]) == 2]

    # Find all the twins by looping through all the pairs
    # and find the ones the have the same values
    twins = [(b1, b2) for b1 in dbl_digits for b2 in dbl_digits if values[b1] == values[b2] and b1 != b2 and b2 in peers[b1]]

    # return the original grid if cannot find twins
    if len(twins) == 0:
        return values
    else:
        for b1, b2 in twins:
            # Find all peers shared by the twins
            relevant_boxes = [box for box in list(set(peers[b1] & peers[b2]))]
            
            # Make sure the twins still have double values throughout the loop
            if len(values[b1]) == 2:
                digit1, digit2 = values[b1] # Grab the digits before the loop
    
                for box in relevant_boxes:
                    value = values[box].replace(digit1, '').replace(digit2, '')
                    values = assign_value(values, box, value)
    
    n_unsolved_boxes_after = len([box for box in values if len(values[box]) > 1])
    print('Naked Twins solved {0} boxes'.format(n_unsolved_boxes_before - n_unsolved_boxes_after))       
    return values
                
    

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = dict(zip(boxes, grid))
    values = {key: '123456789' if item == '.' else item for key, item in values.items()}
    return values

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    
    width = 1+max(len(values[s]) for s in boxes) # set the width to max possible solutions + 1
    line = '+'.join(['-'*(width*3)]*3) # Create the horizontal line
    
    for r in rows:
        # Add the vertical line if the values are between 3 and 6
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '') for c in cols))
        # Add the horizontal line if it's C and F
        if r in 'CF': 
            print(line)
    return

def eliminate(values):
    """
    The function to eliminate known solution from the appropriate solution space
    """
    # Find all the boxes with known solution already
    solved_boxes = [box for box, value in values.items() if len(value) == 1]
    
    n_unsolved_boxes_before = 81 - len(solved_boxes)
    # Loop through each solved box and remove the solution from its peers
    for b in solved_boxes:
        for s in peers[b]:
            new_value = values[s].replace(values[b], '')
            values = assign_value(values, s, new_value)
    
    n_unsolved_boxes_after = len([box for box in values if len(values[box]) > 1])
    print('eliminate solved {0} boxes'.format(n_unsolved_boxes_before - n_unsolved_boxes_after))
    return values


def only_choice(values):
    """
    Function to find unique possible solution in the boxes
    """
    
    n_unsolved_boxes_before = len([box for box in values if len(values[box]) > 1])
    
    # loop through each unit and see if any possible solution is unique to the box
    for units in unitlist:
        for digit in '123456789':
            # For each digit, save the boxes that contain it as possible solution
            choices = [box for box in units if digit in values[box]]

            # If there is only one box in the space that contain the digit, assign it as solution
            if len(choices) == 1:
                values = assign_value(values, choices[0], digit)
    
    n_unsolved_boxes_after = len([box for box in values if len(values[box]) > 1])
    print('only_choice solved {0} boxes'.format(n_unsolved_boxes_before - n_unsolved_boxes_after))
    
    return values
            
def reduce_puzzle(values):
    """
    A loop to apply eliminate and only_choice repeatedly until it is stalled
    """
    
    stalled = False
    while not stalled:
        # save the number of unsolved boxes before
        n_unsolved_before = len([box for box in values if len(values[box]) > 1])
        
        # Apply the two strategies
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        
        # save the number of unsovled boxes after
        n_unsolved_after = len([box for box in values if len(values[box]) > 1])
        
        # See if unsolved boxes decreased
        stalled = n_unsolved_before == n_unsolved_after
        
        # If the strategies result in any boxes with no solution, abort the algorithm
        if len([box for box, value in values.items() if len(value) == 0]):
            return None
    return values
        

def search(values):
    # Apply the basic strategies
    values = reduce_puzzle(values)
    
    # if solution tree leads to dead end, stop the search
    if values == None:
        return None
    
    unsolved_boxes = [(box, value) for box, value in values.items() if len(value) > 1]
    
    # If all boxes are solved, return solution
    if len(unsolved_boxes) == 0:
        return values
    
    # Find the unsolved boxes with smallest number of possible solutions
    box, trials = min(unsolved_boxes, key = lambda x: len(x[1]))
    
    # Try each solution
    for trial in trials:
        attempt = values.copy()
        attempt = assign_value(attempt, box, trial)
        
        # Apply the search algorithm again to see if this solution leads to solved puzzle
        solution = search(attempt)
        
        # return the solution if able to find one
        if solution:
            return solution

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    
    values = grid_values(grid) # Convert the string to dictionary form
    solution = search(values) # Apply the search algorithm
    
    if solution:
        return solution
    else:
        return False

# A function to choose the sudoku to solve
# Got the first two sudokus from Udacity exercise, diagonal sudoku was originally provided in the code
def grid_choice(choice):
    if choice == 'easy':
        grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    elif choice == 'hard':
        grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    elif choice == 'diag1':
        grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    elif choice == 'diag2':
        grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    return grid

rows = 'ABCDEFGHI'
cols = '123456789'

# Create boxes and units for the sudoku
boxes = cross(rows, cols)
row_units = [[r + c for c in cols] for r in rows]
col_units = [[r + c for r in rows] for c in cols]
sq_units = [cross(rs, cs) for rs in ['ABC', 'DEF', 'GHI'] for cs in ['123', '456', '789']]
unitlist = row_units + col_units + sq_units
# Add additional units to the unitlist IF the sudoku is a diagonal sudoku

solving_diagonal_sudoku = True
if solving_diagonal_sudoku:
    diag1_units = [[r+c for r, c in zip(rows, cols)]]
    diag2_units = [[r+c for r, c in zip(rows[::-1], cols)]]
    unitlist += diag1_units + diag2_units
    

# Put the units and peers into dictionary
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)

if __name__ == '__main__':

    # Choose a grid to solve
    choice = input('Enter Difficulty:')
    grid = grid_choice(str(choice))
    values = grid_values(grid)
    # Before
    display(values)
    print('\n')


    values = solve(grid)

    # After
    display(values)

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
