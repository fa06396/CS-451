from PSO import pso
from gui import GUI

ps = None
hud = None


def setup():
    global ps, hud, dimension
    canvasX = 500
    canvasY = 500
    currentBtn = 1
    dimension = 2
    size(1260, 720)
    hud = GUI()
    # size(1000,1000)
    ps = pso(canvasSize=[720, 720], numSize=50, numFood=0)
    
def draw():
    background(0)
    ps.update()
    hud.draw()

def mouseClicked():
    '''

    This Code is Inspired from https://github.com/osama-usuf/Interactive-Ant-Colony-Optimization-Simulation

    '''
    global CurrntBtn
    button = hud.mouseHover()
    if (button):
        if (button == 1): #toggle double slit
            ps.birdMaking(dimension)
            hud.toggleButton(button-1)
            return
        elif (button == 2):
            ps.foodMaking(1, 20)
            hud.toggleButton(button-1)
            return
        hud.toggleButton(currBtn-1)
        hud.toggleButton(button-1)
        currBtn = button
        return
    
