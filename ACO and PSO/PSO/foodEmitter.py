from Food import Food
import random


class FoodEmitter():
    def __init__(self, height, dimension):
        self.foods = []
        self.height = height
        self.dimension = dimension

    def addFood(self, numFood, tempConst, numBirds):
        for i in range(numFood):
            food = [random.randint(0, self.height)
                    for i in range(self.dimension)]
            foodFit = random.randint(0, numBirds + tempConst)
            self.foods.append(Food(food, foodFit))
