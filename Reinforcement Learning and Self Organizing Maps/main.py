from grid import Grid
from agent import Agent


class ReinforcementLearning():
    '''Reinforcement Learning Class that has an agent, a grid and uses
    Temporal Difference Learning to train the agent.
    '''

    def __init__(self, n: int, alpha: float, gamma: float, episodes: int) -> None:
        '''Initializes the RL model with alpha and gamma rates
        creates a grid of NxN states and creates an Agent.

        Parameters:
        - self: mandatory reference to this object
        - n: integer the size of the grid
        - alpha: float parameter for Temporal Learning
        - gamma: float parameter for Temporal Learning
        - episodes: integer numer of episodes the Agent needs to complete.

        Returns:
        None
        '''
        self.grid = Grid(n)
        self.agent = Agent(alpha, gamma, n, self.grid)
        self.episodes = episodes

    def run(self) -> None:
        '''Runs the agent for the specified number of episodes

        Parameters:
        - self: mandatory reference to this object

        Returns:
        None
        '''
        self.agent.runAgent(self.episodes, self.grid)


def main():
    n = 10
    alpha = 0.2
    gamma = 0.5
    episodes = 20
    model = ReinforcementLearning(n, alpha, gamma, episodes)
    model.run()


if __name__ == '__main__':
    main()
