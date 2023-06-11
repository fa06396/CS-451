import random
import math
from Bird import bird
from Food import Food
from foodEmitter import FoodEmitter


class pso:
    momentum = 0.1
    accelConst = [0.1, 0.1]

    def __init__(self, canvasSize, numSize, numFood):
        self.birds = []
        self.foods = []
        # self.momentum = momentum
        # self.accelConst = accelConst
        tempConst = 20
        self.height = canvasSize[1]
        self.width = canvasSize[0]
        self.numBirds = numSize
        self.dimension = 2
        self.foodApproxLoc = 1000
        self.gBest = [random.randint(0, self.height)
                      for i in range(self.dimension)]
        self.gBestValue = 0
        self.foodMaking(numFood, tempConst)
        self.birdMaking(self.dimension)
        self.countFoundFood = 0
        self.gBestFound = False

    def foodMaking(self, numFood, tempConst):
        for i in range(numFood):
            food = [random.randint(0, self.height)
                    for i in range(self.dimension)]
            foodFit = random.randint(0, self.numBirds + tempConst)
            self.foods.append(Food(food, foodFit))

    def update(self):
        for i in self.foods:
            i.render()
        for i in self.birds:
            i.render()
        self.optimization()

    def birdMaking(self, dimension):
        for i in range(self.numBirds):
            tempBird = bird(velocity=[random.randint(-1, 1) for i in range(dimension)], position=[random.randint(0, self.height) for i in range(self.dimension)],  pBest=[
                            random.randint(0, self.height) for i in range(dimension)], lbest=[random.randint(0, self.height) for i in range(dimension)], pBestValue=0)

            self.birds.append(tempBird)

    def updateVelocity(self, bird):
        for i in range(self.dimension):
            bird.velocity[i] = self.momentum * bird.velocity[i] + self.accelConst[0] * random.random() * (
                bird.pBest[i] - bird.position[i]) + self.accelConst[1] * random.random() * (self.gBest[i] - bird.position[i])
        # return bird

    def updatePosition(self, bird):
        for i in range(self.dimension):
            bird.position[i] = bird.position[i] + bird.velocity[i]
            if bird.position[i] > self.height:
                bird.position[i] = self.height
            if bird.position[i] < 0:
                bird.position[i] = 0
        # return bird

    def updatepBest(self, bird):
        for food in self.foods:
            temp = 0
            for j in range(self.dimension):
                temp += math.pow((food.position[j] - bird.position[j]), 2)
            temp = math.sqrt(temp)

            if temp < self.foodApproxLoc and bird.pBestValue < food.value:
                if bird.foundFood == False:
                    self.countFoundFood += 1
                    bird.foundFood = True
                    print(self.countFoundFood,
                          " birds found food at location", food.position)
                bird.pBest = food.position
                bird.pBestValue = food.value

            if bird.pBestValue > self.gBestValue:
                self.gBest = bird.pBest
                self.gBestValue = bird.pBestValue
            self.gBestFound = True
        # return bird

    def optimization(self):
        # while self.countFoundFood < self.numBirds:
        for i in self.birds:
            if self.gBestFound == False:
                self.gBest = [random.randint(
                    0, self.height) for j in range(self.dimension)]
                i.pBest = [random.randint(
                    0, self.height) for j in range(self.dimension)]
            self.updateVelocity(i)
            self.updatePosition(i)
            self.updatepBest(i)
        for i in range(len(self.birds)):
            self.updatepBest(self.birds[i])


# if __name__ == "__main__":
#     # test
#     pso = PSO(momentum=0.5, accelConst=[0.5, 0.5], canvasSize=[
#               100, 100], numSize=20, numFood=2)
#     pso.optimization()
