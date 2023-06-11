from state import State
import random


class Grid():
    '''
    The NxN grid that will be used for the Agent to run on.
    '''

    def __init__(self, n: int, redStates=0.2, greenStates=0.05) -> None:
        '''Initializes the grid by creating NxN list of States
        adds Terminal states with Red states based on percentage of red states
        and one green state. Also calculates a starting position for the Agent.

        Parameters:
        - self: mandatory reference to this object
        - n: integer the size of the grid
        - redStates: float percentage of red states in the grid
        -greenStates: float percentage of green states in the grid

        Returns:
        None
        '''
        self.grid = [[State(j, i, reward=-1) for i in range(n)]
                     for j in range(n)]
        self.redStates = int(redStates * n * n)
        self.greenStates = int(greenStates * n * n)
        self.dimension = n
        self.green = set()
        self.__addTerminals(n)
        self.__getStartPos(n)

    def __addTerminals(self, n: int) -> None:
        '''Adds the absorbing (Terminal) States.

        Parameters:
        - self: mandatory reference to this object
        - n: integer the size of the grid

        Returns:
        None
        '''
        self.marked = set()
        for reds in range(self.redStates):
            i = random.randint(0, n-1)
            j = random.randint(0, n-1)
            while (i, j) in self.marked:
                i = random.randint(0, n-1)
                j = random.randint(0, n-1)
            currentState = self.grid[i][j]
            currentState.isTerminal = True
            currentState.reward = -100
            currentState.val = -1
            self.marked.add((i, j))
        for green in range(self.greenStates):
            i = random.randint(0, n-1)
            j = random.randint(0, n-1)
            while (i, j) in self.marked:
                i = random.randint(0, n-1)
                j = random.randint(0, n-1)
            currentState = self.grid[i][j]
            currentState.isTerminal = True
            currentState.reward = 100
            currentState.val = 1
            self.marked.add((i, j))
            self.green.add((i, j))

    def __getStartPos(self, n: int) -> None:
        '''Randomly assigns the starting position for the agent.

        Parameters:
        - self: mandatory reference to this object
        - n: integer the size of the grid

        Returns:
        None
        '''
        i = random.randint(0, n-1)
        j = random.randint(0, n-1)
        while (i, j) in self.marked:
            i = random.randint(0, n-1)
            j = random.randint(0, n-1)
        self.StartPos = self.grid[i][j]
        print(f'Start at Coord = {(i, j)}')

    def __getitem__(self, index: 'list[int, int]') -> 'State':
        '''Returns the State at the ith and jth index of the Grid.

        Parameters:
        - self: mandatory reference to this object
        - index: list of [i, j] indices that the state is required for.

        Returns:
        State object at the index
        '''
        i, j = index
        return self.grid[i][j]

    def __len__(self) -> int:
        '''Returns the length of the grid.

        Parameters:
        - self: mandatory reference to this object

        Returns:
        Length of the grid
        '''
        return len(self.grid)

    def printGrid(self):
        '''Prints the Grid on terminal.

        Parameters:
        - self: mandatory reference to this object

        Returns:
        None
        '''
        for i in range(self.dimension):
            for j in range(self.dimension):
                print(self.grid[i][j].val, end=' ')
            print()
