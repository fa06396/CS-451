class bird:
    r = 255
    g = 255
    b = 255

    def __init__(self, velocity, pBestValue, pBest, lbest, position):
        self.velocity = velocity
        self.position = position
        self.pBest = pBest
        self.lbest = lbest
        self.pBestValue = pBestValue
        self.foundFood = False

    def render(self):
        fill(self.r, self.g, self.b)
        ellipse(self.position[0], self.position[1], 10, 10)

    def updateVelocity(self):
        pass

    def updatePosition(self):
        pass

    def updatePBest(self):
        pass

    def fitness(self):
        return 0
