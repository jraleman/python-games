"""
Name: Zombie Apocalypse mini-project.
Author: jraleman
Year: 2014
"""

try:
    import poc_grid
    import poc_queue
    import poc_zombie_gui
except ImportError:
    import assets.poc_grid as poc_grid
    import assets.poc_queue as poc_queue
    import assets.poc_zombie_gui as poc_zombie_gui
import random


# Global constants.
EMPTY = 0
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"

class Grid:
    """
    Implementation of 2D grid of cells
    Includes boundary handling
    """

    def __init__(self, grid_height, grid_width):
        """
        Initializes grid to be empty, take height and width of grid as
        parameters, idexed by rows (left to right),
        then by columns (top to bottom).
        """
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._cells = [[EMPTY for dummy_col in range(self._grid_width)] \
                        for dummy_row in range(self._grid_height)]

    def __str__(self):
        """
        Return multi-line string representation for grid.
        """
        ans = ""
        for row in range(self._grid_height):
            ans += str(self._cells[row]) + '\n'
        return ans

    def get_grid_width(self):
        """
        Return the width of the grid for use in the GUI.
        """
        return self._grid_width

    def get_grid_height(self):
        """
        Return the height of the grid for use in the GUI
        """
        return self._grid_height

    def clear(self):
        """
        Clears grid to be empty.
        """
        self._cells = [[EMPTY for dummy_col in range(self._grid_width)] \
                       for dummy_row in range(self._grid_height)]

    def set_empty(self, row, col):
        """
        Set cell with the index (row, col) to be empty.
        """
        self._cells[row][col] = EMPTY

    def set_full(self, row, col):
        """
        Set cell with the index (row, col) to be full.
        """
        self._cells[row][col] = FULL

    def is_empty(self, row, col):
        """
        Checks whether cell with index (row, col) is empty.
        """
        return self._cells[row][col] == EMPTY

    def four_neighbors(self, row, col):
        """
        Returns horizontal/vertical neighbours of the cell (row, col).
        """
        ans = []
        if row > 0:
            ans.append((row - 1, col))
        if row < self._grid_height - 1:
            ans.append((row + 1, col))
        if col > 0:
            ans.append((row, col - 1))
        if col < self._grid_width - 1:
            ans.append((row, col + 1))
        return ans

    def eight_neighbors(self, row, col):
        """
        Returns horizontal/vertical neighbours of the cell (row, col),
        as well as diagonal neighbours.
        """
        ans = []
        if row > 0:
            ans.append((row - 1, col))
        if row < self._grid_height - 1:
            ans.append((row + 1, col))
        if col > 0:
            ans.append((row, col - 1))
        if col < self._grid_width - 1:
            ans.append((row, col + 1))
        if (row > 0) and (col > 0):
            ans.append((row - 1, col - 1))
        if (row > 0) and (col < self._grid_width - 1):
            ans.append((row - 1, col + 1))
        if (row < self._grid_height - 1) and (col > 0):
            ans.append((row + 1, col - 1))
        if (row < self._grid_height - 1) and (col < self._grid_width - 1):
            ans.append((row + 1, col + 1))
        return ans

    def get_index(self, point, cell_size):
        """
        Takes point in screen coordinates and returns index
        of the containing cell.
        """
        return (point[1] / cell_size, point[0] / cell_size)


class Queue:
    """
    A simple implementation of a FIFO (first in - first out) queue.
    """

    def __init__(self):
        """
        Initialize the queue.
        """
        self._items = []

    def __len__(self):
        """
        Return the number of items in the queue.
        """
        return len(self._items)

    def __iter__(self):
        """
        Create an iterator for the queue.
        """
        for item in self._items:
            yield item

    def enqueue(self, item):
        """
        Add item to the queue.
        """
        self._items.append(item)

    def dequeue(self, item):
        """
        Remove and return the least recently inserted item.
        """
        return self._items.pop(0)

    def clear(self):
        """
        Remove all items from the queue.
        """
        self._items = []


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles.
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None,
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies.
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
            self._obstacle_list = obstacle_list
        else:
            self._obstacle_list = []
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)
        else:
            self._human_list = []

    def clear(self):
        """
        Set cells in obstacle grid to be empty.
        Reset zombie and human lists to be empty.
        """
        self._zombie_list = []
        self._human_list = []
        poc_grid.Grid.clear(self)

    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list.
        """
        self._zombie_list.append((row, col))

    def num_zombies(self):
        """
        Return number of zombies.
        """
        return len(self._zombie_list)

    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list.
        """
        self._human_list.append((row, col))

    def num_humans(self):
        """
        Return number of humans.
        """
        return len(self._human_list)

    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human_list:
            yield human

    def obstacle(self):
        """
        Generator that yields the list of obstacles.
        """
        for obstacle in self._obstacle_list:
            yield obstacle

    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field.
        Distance at member of entity_queue is zero.
        Shortest paths avoid obstacles and use distance_type distances.
        """
        # Same size as the grid and initialized with artificially high values.
        distance_field =[[self._grid_height * self._grid_width \
                        for dummy_col in range(self._grid_width)] \
                        for dummy_row in range(self._grid_height)]

        # Grid visited initialized as to be empty.
        visited = poc_grid.Grid(self._grid_height, self._grid_width)
        for obstacle in self.obstacle():
            visited.set_full(obstacle[0], obstacle[1])

        # Creates a copy of the human/zombie list.
        boundary = poc_queue.Queue()
        if entity_type == ZOMBIE:
            list_type = self._zombie_list
        elif entity_type == HUMAN:
            list_type = self._human_list

        # Check if the cell is passable and update the neighbour's distance.
        for item in list_type:
            boundary.enqueue(item)
            visited.set_full(item[0], item[1])
            distance_field[item[0]][item[1]] = 0

        # Breadth-first search
        while boundary:
            cell = boundary.dequeue()
            neighbors = visited.four_neighbors(cell[0], cell[1])
            for resident in neighbors:
                if visited.is_empty(resident[0], resident[1]):
                    distance_field[resident[0]][resident[1]] = \
                    min(distance_field[resident[0]][resident[1]],
                    distance_field[cell[0]][cell[1]] + 1)
                    visited.set_full(resident[0], resident[1])
                    boundary.enqueue(resident)
        return distance_field

    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        temp_human_list = []
        for human in self.humans():
            neighbors = self.eight_neighbors(human[0], human[1])
            # Store current position.
            distance = [zombie_distance[human[0]][human[1]]]
            location = [human]

            for resident in neighbors:
                if self.is_empty(resident[0], resident[1]):
                    # Store rest of 8 other positions if not occupied.
                    distance.append(zombie_distance[resident[0]][resident[1]])
                    location.append(resident)
            # Find the current safest location, move there.
            safest = location[distance.index(max(distance))]
            self.set_empty(human[0], human[1])
            temp_human_list.append(safest)

        self._human_list = temp_human_list

    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        temp_zombie_list = []
        # For zombie in self.zombies()
        for zombie in self._zombie_list:
            neighbors = self.four_neighbors(zombie[0], zombie[1])
            distance = [human_distance[zombie[0]][zombie[1]]]
            location = [zombie]

            for resident in neighbors:
                if self.is_empty(resident[0], resident[1]):
                    # Store rest of four (4) other positions if not occupied.
                    distance.append(human_distance[resident[0]][resident[1]])
                    location.append(resident)
            # Find the current most closest location, and move there.
            closest = location[distance.index(min(distance))]
            self.set_empty(zombie[0], zombie[1])
            temp_zombie_list.append(closest)
        self._zombie_list = temp_zombie_list

poc_zombie_gui.run_gui(Zombie(30, 40))
