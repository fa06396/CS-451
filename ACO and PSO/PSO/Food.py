class Food:
    foodSize = 10

    def __init__(self, position, value):
        self.position = position
        self.value = value
        self.posx = position[0]
        self.posy = position[1]

    def render(self):
        fill(255, 255, 255)
        square(self.posx, self.posy, self.foodSize)
        # image(self.img, self.loc.x, self.loc.y)
