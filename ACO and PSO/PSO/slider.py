'''

This File is taken from https://github.com/osama-usuf/Interactive-Ant-Colony-Optimization-Simulation

'''

from button import Button
from Bird import bird
from Food import Food
from PSO import pso


class Slider:
    sliderCount = 0

    def __init__(self, label, low, high, default, bg):
        '''slider has range from low to high
        and is set to default'''
        self.low = low
        self.high = high
        self.val = default
        self.clicked = False
        self.label = label  # blank label
        self.bg = bg
        self.x = bg[0] + (bg[2]-120)/2
        if(Slider.sliderCount == 0):
            self.y = bg[1] + (Button.buttonCount+1)*Button.buttonSpacing
            Slider.sliderCount = Button.buttonCount
        else:
            self.y = bg[1] + (Slider.sliderCount+1)*Button.buttonSpacing
        self.rectx = self.x + map(self.val, self.low, self.high, 0, 120)
        self.recty = self.y - 10
        Slider.sliderCount += 1

    def draw(self):
        '''updates the slider and returns value'''
        # gray line behind slider
        strokeWeight(4)
        stroke(200)
        line(self.x, self.y, self.x + 120, self.y)
        # press mouse to move slider
        if mousePressed and dist(mouseX, mouseY, self.rectx, self.recty) < 20:
            self.rectx = mouseX
        # constrain rectangle
        self.rectx = constrain(self.rectx, self.x, self.x + 120)
        # draw rectangle
        strokeWeight(1)
        stroke(0)
        fill(255)
        rect(self.rectx, self.recty, 15, 20)
        self.val = map(self.rectx, self.x, self.x + 120, self.low, self.high)
        # draw label
        fill(0)
        textSize(12)
        text(int(self.val), self.rectx+8, self.recty+8)
        # text label
        fill(255, 255, 255)
        text(self.label, self.x+60, self.y+20)
        if(self.label == 'Red Intensity'):
            bird.r = self.val
        elif(self.label == 'Green Intensity'):
            bird.g = self.val
        elif(self.label == 'Blue Intensity'):
            bird.b = self.val
        elif(self.label == 'Food Size'):
            Food.foodSize = self.val
        elif(self.label == 'Momentum'):
            pso.momentum = self.val / 100
        elif(self.label == 'Accel Const 1'):
            pso.accelConst[0] = self.val / 1000
        elif(self.label == 'Accel Const 2'):
            pso.accelConst[1] = self.val / 1000
