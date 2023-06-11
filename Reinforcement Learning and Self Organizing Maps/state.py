class State():
    '''A State that stores its current value, wether it is an absorbing
    state (terminal) or, its reward and the x,y coordinates on the grid.
    '''

    def __init__(self, x: int, y: int, val=0, reward=0) -> None:
        '''Initializes a state with value and reward as 0 by defualt
        and the coordinates of the state are stored.

        Parameters:
        - self: mandatory reference to this object
        - x: integer horizontal cell location of the state
        - y: integer vertical cell location of the state
        - val: integer the initial value of the state
        - reward: integer the intial reward of the state

        Returns:
        None
        '''
        self.val = val
        self.isTerminal = False
        self.reward = reward
        self.boltzman = {}
        self.coord = (x, y)
