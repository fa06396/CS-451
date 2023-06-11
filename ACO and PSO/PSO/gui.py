'''

This File is taken from https://github.com/osama-usuf/Interactive-Ant-Colony-Optimization-Simulation

'''


from button import Button
from slider import Slider


class GUI:  # resolution is hard-coded for now, can be generalized by adding association to Map
    def __init__(self):
        self.buttons = []
        self.sliders = []
        self.bg = [1080, 0, 200, 720]  # x,y,w,h
        # # #Toggle Buttons
        self.buttons.append(Button('Add More Birds', self.bg))
        self.buttons[0].pressed = True
        self.buttons.append(Button('Add More Food', self.bg))
        self.buttons[0].pressed = True
        # Sliders
        self.sliders.append(Slider('Red Intensity', 0, 255, 255, self.bg))
        self.sliders.append(Slider('Green Intensity', 0, 255, 255, self.bg))
        self.sliders.append(Slider('Blue Intensity', 0, 255, 255, self.bg))
        self.sliders.append(Slider('Momentum', 0, 100, 100, self.bg))
        self.sliders.append(Slider('Accel Const 1', 0, 100, 100, self.bg))
        self.sliders.append(Slider('Accel Const 2', 0, 100, 100, self.bg))
        self.sliders.append(Slider('Food Size', 0, 50, 10, self.bg))
        self.tit = '    Particle Swam Optimization (PSO)\n'
        self.crs = '    Computational Intelligence\n'
        self.auth_1 = '    Ronit Kumar Kataria - rk06451\n'
        self.auth_2 = '    Faraz Ali - fa06396'
        self.crdt = self.crs+self.tit+self.auth_1+self.auth_2

    def draw(self):
        text
        noStroke()
        rectMode(CORNER)
        fill(77, 155, 247, 100)
        rect(*self.bg)
        self.drawElements()
        textSize(11)
        fill(255)
        text(self.crdt, self.bg[0], self.bg[1] +
             (Slider.sliderCount+1)*Button.buttonSpacing, 160, 120)

    def drawElements(self):
        for i in self.buttons:
            i.draw()
        for i in self.sliders:
            i.draw()

    def mouseHover(self):
        for i in self.buttons:
            if (i.mouseHover()):
                return i.id
        return None

    def toggleButton(self, id):
        self.buttons[id].pressed = not self.buttons[id].pressed
