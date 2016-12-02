"""
Loyd's Fifteen puzzle - solver and visualizer
Author: jraleman
Year: 2014
"""

# Loyd's Fifteen puzzle - solver and visualizer.
# Note that solved configuration has the blank (zero) tile in upper left.
# Use the arrows key to swap this tile with its neighbors.

try:
    import poc_fifteen_gui
except ImportError:
    import assets.poc_fifteen_gui as poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle.
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width.
        Returns a Puzzle object.
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                     for col in range(self._width)]
                    for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle.
        Returns a string.
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans


    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height.
        Returns an integer.
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width.
        Returns an integer.
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos.
        Returns an integer.
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos.
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving.
        Returns a Puzzle object.
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle


    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at.
        position (solved_row, solved_col) when the puzzle is solved.
        Returns a tuple of two integers.
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found."

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string.
        """
        row, col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert col > 0, "move off grid: " + direction
                self._grid[row][col] = self._grid[row][col - 1]
                self._grid[row][col - 1] = 0
                col -= 1
            elif direction == "r":
                assert col < self._width - 1, "move off grid: " + direction
                self._grid[row][col] = self._grid[row][col + 1]
                self._grid[row][col + 1] = 0
                col += 1
            elif direction == "u":
                assert row > 0, "move off grid: " + direction
                self._grid[row][col] = self._grid[row - 1][col]
                self._grid[row - 1][col] = 0
                row -= 1
            elif direction == "d":
                assert row < self._height - 1, "move off grid: " + direction
                self._grid[row][col] = self._grid[row + 1][col]
                self._grid[row + 1][col] = 0
                row += 1
            else:
                assert False, "invalid direction: " + direction


    ##################################################################
    # Phase one methods

    def move(self, target_row, target_col, row, column):
        '''
        Place a tile at target position;.
        Target tile's current position must be either above the target position
        (k < i) or on the same row to the left (i = k and l < j);
        Returns a move string.
        '''
        move_it = ''
        combo = 'druld'

        # Calculate deltas.
        column_delta = target_col - column
        row_delta = target_row - row

        # Always move up at first.
        move_it += row_delta * 'u'

        # Both tiles in the same column, combo 'ld' shall go first.
        if column_delta == 0:
            move_it += 'ld' + (row_delta - 1) * combo
        else:
            # Tile is on the left from target.
            if column_delta > 0:
                move_it += column_delta * 'l'
                if row == 0:
                    move_it += (abs(column_delta) - 1) * 'drrul'
                else:
                    move_it += (abs(column_delta) - 1) * 'urrdl'
            # Tile is on the right from target.
            elif column_delta < 0:
                move_it += (abs(column_delta) - 1)  * 'r'
                if row == 0:
                    move_it += abs(column_delta) * 'rdllu'
                else:
                    move_it += abs(column_delta) * 'rulld'
            # Apply common move as last
            move_it += row_delta * combo
        return move_it

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1).
        Returns a boolean.
        """

        if self.get_number(target_row, target_col) == 0:
            # All tiles in row (target_row) to the right position.
            for columns in range(target_col + 1, self.get_width()):
                if not (target_row, columns) == \
                self.current_position(target_row, columns):
                    return False
            # Tiles in row (target_row + 1) or below are positioned at
            # their solved location.
            if not target_row + 1 == self.get_height():
                for columns_below in range (0, self.get_width()):
                    # If tile is in last row, no need to check for more.
                    if not (target_row + 1, columns_below) == \
                    self.current_position(target_row + 1, columns_below):
                        return False
        return True


    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position.
        Updates puzzle and returns a move string.
        """
        row, column = self.current_position(target_row, target_col)
        move_it = self.move(target_row, target_col, row, column)
        self.update_puzzle(move_it)
        assert self.lower_row_invariant(target_row, target_col - 1)
        return move_it


    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1).
        Updates puzzle and returns a move string.
        """
        move_it = 'ur'
        self.update_puzzle(move_it)
        row, column = self.current_position(target_row, 0)

        # Target tile already in place.
        if row == target_row and column == 0:
            # Move tile zero (0) to the right end of that row.
            step = (self.get_width() - 2) * 'r'
            self.update_puzzle(step)
            move_it += step
        else:
            step = self.move(target_row - 1, 1, row, column)
            step += 'ruldrdlurdluurddlu' + (self.get_width() - 1) * 'r'
            self.update_puzzle(step)
            move_it += step
        return move_it


    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1).
        Returns a boolean.
        """
        # If zero (0) tile is not in expected column, no need to check for more.
        if not self.get_number(0, target_col) == 0:
            return False
        for column in range(self.get_width()):
            for row in range(self.get_height()):
                # Exclude the tiles we aren't interested,
                # then check if the rest of tiles is solved
                if (row == 0 and column > target_col) or \
                (row == 1 and column >= target_col) or row > 1:
                    if not (row, column) == self.current_position(row, column):
                        return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # Row 1 is limited case of general row invariant check,
        # If row 1 is not solved, no need to check for more
        if not self.lower_row_invariant(1, target_col):
            return True
        # Check if all tiles in rows bellow row 1 are positioned
        # at their solved location
        for column in range(0, self.get_width()):
            for row in range(2, self.get_height()):
                if not (row, column) == self.current_position(row, column):
                    return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column.
        Updates puzzle and returns a move string.
        """
        move_it = 'ld'
        self.update_puzzle(move_it)
        row, column = self.current_position(0, target_col)
        # Got lucky, target tile already in place.
        if row == 0 and column == target_col:
            return move_it
        # Target tile to position (1, target_col - 1)
        # and move for the 2x3 puzzle.
        else:
            step = self.move(1, target_col - 1, row, column)
            step += 'urdlurrdluldrruld'
            self.update_puzzle(step)
            move_it += step
        return move_it

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        row, column = self.current_position(1, target_col)
        move_it = self.move(1, target_col, row, column)
        move_it += 'ur'
        self.update_puzzle(move_it)
        return move_it


    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        move_it = ''
        first_step = ''

        if self.get_number(1, 1) == 0:
            first_step += 'ul'
            self.update_puzzle(first_step)
            # Got lucky, all tiles are already in place
            if (0, 1) == self.current_position(0, 1) and \
            (1, 1) == self.current_position(1, 1):
                return first_step
            # Pick a move depending on current configuration
            if self.get_number(0, 1) < self.get_number(1, 0):
                move_it += 'rdlu'
            else:
                move_it += 'drul'
            self.update_puzzle(move_it)
        return first_step + move_it

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move_it = ''
        # Need 0 tile in the right lower corner.
        row = self.get_height() - 1
        column = self.get_width() - 1
        row_current, column_current = self.current_position(0, 0)
        # Calculate deltas.
        column_delta = column_current - column
        row_delta = row_current - row
        step = abs(column_delta) * 'r' + abs(row_delta) * 'd'
        self.update_puzzle(step)
        move_it += step
        # Bottom m-2 rows in order from bottom to top and right to left
        for dummy_row in range(row, 1, -1):
            for dummy_column in range(column, 0, -1):
                move_it += self.solve_interior_tile(dummy_row, dummy_column)
            move_it += self.solve_col0_tile(dummy_row)
        # Rightmost n-2 columns of the top two rows in a bottom to top
        # and right to left order
        for dummy_column in range(column, 1, -1):
            move_it += self.solve_row1_tile(dummy_column)
            move_it += self.solve_row0_tile(dummy_column)
        move_it += self.solve_2x2()
        return move_it

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))
