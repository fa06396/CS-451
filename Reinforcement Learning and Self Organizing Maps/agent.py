import random
import math
from grid import Grid
import tkinter as tk
import time


root = tk.Tk()
canvas = tk.Canvas(root, width=800, height=800, bg="black")
canvas.pack()


def draw(currentPos: 'tuple (int, int)', grid: 'Grid', cellSize: int) -> None:
    '''Global Function that is used to draw grid at each iteration

    Parameters:
    - currentPos: tuple of current index of agent
    - grid: Grid the grid to draw
    - cellSize: integer cell size to display depending on the size of the grid

    Returns:
    None
    '''
    canvas.delete('all')
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i, j].reward == 100:
                col = 'green'
            elif grid[i, j].reward == -100:
                col = 'red'
            else:
                col = 'white'
            if grid[i, j].coord == currentPos:
                col = 'blue'
            x1 = j * cellSize
            y1 = i * cellSize
            x2 = x1 + cellSize
            y2 = y1 + cellSize
            canvas.create_rectangle(x1, y1, x2, y2, fill=col)
            cell_value = grid[i, j].val
            x_center = (x1 + x2) // 2
            y_center = (y1 + y2) // 2
            canvas.create_text(x_center, y_center, text=str(
                cell_value), font=("Arial", 8))
    canvas.update()
    time.sleep(0.1)


class Agent():
    '''The RL Agent that moves around the grid and takes its decisions using
    Temporal Differnece.
    '''

    def __init__(self, alpha: float, gamma: float, n: int, grid: 'Grid') -> None:
        '''Initializes the agent with alpha and gamma rates
        and provides the starting position of the agent in the grid.

        Parameters:
        - self: mandatory reference to this object
        - alpha: float parameter for Temporal Learning
        - gamma: float parameter for Temporal Learning
        - n: integer the size of the grid
        - grid: Grid the grid the agent is supposed to perform actions on

        Returns:
        None
        '''
        self.cellSize = 800 // n
        self.alpha = alpha
        self.gamma = gamma
        self.dimension = n-1
        self.currentState = grid.StartPos
        self.temperature = 1

    def valueFunction(self, action: str, grid: 'Grid') -> None:
        '''Updates the value of the current state based on the action taken
        by the RL Agent.

        Parameters:
        - self: mandatory reference to this object
        - action: string the action taken by the agent
        - grid: Grid the grid the agent is supposed to perform actions on

        Returns:
        None
        '''
        actions = {
            'left': (0, -1),
            'right': (0, 1),
            'up': (-1, 0),
            'down': (1, 0)
        }
        i, j = actions[action]
        i += self.currentState.coord[0]
        j += self.currentState.coord[1]
        nextState = grid[i, j]
        self.currentState.val = self.currentState.val + \
            self.alpha * (nextState.reward + (self.gamma *
                                              nextState.val) - self.currentState.val)
        self.currentState = nextState

    def getAction(self, grid: 'Grid') -> str:
        '''Provides the next best action that the Agent can take.

        Parameters:
        - self: mandatory reference to this object
        - grid: Grid the grid the agent is supposed to perform actions on

        Returns:
        Action String
        '''
        i, j = self.currentState.coord
        actions = {}
        if i == 0:
            if j == self.dimension:
                actions['left'] = grid[i, j-1].val
                actions['down'] = grid[i+1, j].val
            elif j == 0:
                actions['right'] = grid[i, j+1].val
                actions['down'] = grid[i+1, j].val
            else:
                actions['left'] = grid[i, j-1].val
                actions['down'] = grid[i+1, j].val
                actions['right'] = grid[i, j+1].val
        elif i == self.dimension:
            if j == self.dimension:
                actions['left'] = grid[i, j-1].val
                actions['up'] = grid[i-1, j].val
            elif j == 0:
                actions['right'] = grid[i, j+1].val
                actions['up'] = grid[i-1, j].val
            else:
                actions['left'] = grid[i, j-1].val
                actions['up'] = grid[i-1, j].val
                actions['right'] = grid[i, j+1].val
        else:
            if j == self.dimension:
                actions['left'] = grid[i, j-1].val
                actions['up'] = grid[i-1, j].val
                actions['down'] = grid[i+1, j].val
            elif j == 0:
                actions['down'] = grid[i+1, j].val
                actions['right'] = grid[i, j+1].val
                actions['up'] = grid[i-1, j].val
            else:
                actions['left'] = grid[i, j-1].val
                actions['up'] = grid[i-1, j].val
                actions['right'] = grid[i, j+1].val
                actions['down'] = grid[i+1, j].val
        return self.boltzmanDistribution(i, j, actions, grid)

    def boltzmanDistribution(self, i: int, j: int, actions: 'dict[str:float]', grid: 'Grid'):
        '''Calculates Boltzman Distribution for each state and returns best action

        Parameters:
        - self: mandatory reference to this object
        - i: integer row of current State
        - j: integer column of current State
        - actions: dictionary of action value pair for each possible action
        - grid: Grid the grid the agent is supposed to perform actions on

        Returns:
        Action String
        '''
        e = math.e
        denominator = 0
        possibleActions = [a for a in actions]
        for _ in actions:
            denominator += e ** (actions[_] / self.temperature)
        for _ in possibleActions:
            grid[i, j].boltzman[_] = (
                e ** (actions[_] / self.temperature)) / denominator
        if self.temperature < 0.1:
            grid[i, j].boltzman = dict(
                sorted(grid[i, j].boltzman.items(), key=lambda x: x[1], reverse=True))
            for _ in grid[i, j].boltzman:
                return _
        else:
            grid[i, j].boltzman = dict(
                sorted(grid[i, j].boltzman.items(), key=lambda x: x[1]))
            randomProb = random.random()
            prev = 0
            for vals in grid[i, j].boltzman:
                if prev + grid[i, j].boltzman[vals] >= randomProb:
                    return vals
                else:
                    prev += grid[i, j].boltzman[vals]

    def runAgent(self, episodes: int, grid: 'Grid') -> None:
        '''Runs the agent for the specified number of episodes

        Parameters:
        - self: mandatory reference to this object
        - episodes: integer the number of episodes that agent needs to run on
        - grid: Grid the grid the agent is supposed to perform actions on

        Returns:
        None
        '''
        for e in range(episodes):
            grid.printGrid()
            print(f'Episode = {e}')
            self.currentState = grid.StartPos
            while not self.currentState.isTerminal:
                action = self.getAction(grid)
                self.valueFunction(action, grid)
                draw(self.currentState.coord, grid, self.cellSize)
            print(f'Ending Coord = {self.currentState.coord}')
            if self.temperature >= 0.1:
                self.temperature = self.temperature * 0.95
        print(grid.green)
        print(self.currentState.coord in grid.green)
