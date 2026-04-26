import pyglet
from pyglet import window, shapes, font
from DIPPID import SensorUDP
import random
import time

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PORT = 5700
SQUARE_SIZE = 20

sensor = SensorUDP(PORT)

win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)

#load cool font (https://www.1001fonts.com/pixel-game-font.html)
font.add_file('Pixel Game.otf')

#initial values
score = 0
direction = "R" #one of "R", "L", "U", "D"
end = False

#shapes
head = shapes.Rectangle(400, 400, SQUARE_SIZE, SQUARE_SIZE, (0, 100, 50))
body = shapes.Rectangle(400, 400, SQUARE_SIZE, SQUARE_SIZE, (0, 150, 100))
food = shapes.Rectangle(random.randint(0, (WINDOW_WIDTH - SQUARE_SIZE)), random.randint(0, (WINDOW_HEIGHT - SQUARE_SIZE)), SQUARE_SIZE, SQUARE_SIZE, (200, 0, 0))

#coordinated of body segments
#FIXME should be empty at the start, just for testing
segments = [[380, 400], [360, 400], [340, 400]]


#play
@win.event
def on_draw():
    #global variables we want to use in this function
    global direction
    global segments
    global score
    global end
    #FIXME add some?

    if not end:

        win.clear()

        #update body positions: #TODO test
        #each takes the position of the one in front, the first takes the position of the head
        print(f"segments: {segments}")
        for i in range(len(segments)-1, 0, -1):
            tempx = segments[i-1][0]
            tempy = segments[i-1][1]
            segments[i] = [tempx, tempy]
            body.x = segments[i][0]
            body.y = segments[i][1]
            body.draw()
        if not segments == []:
            segments[0][0] = head.x
            segments[0][1] = head.y
            body.x = head.x
            body.y = head.y
            body.draw()

        # check if sensor data is received
        if not sensor.get_capabilities() == []:

            #Threshold for smooter operation
            #snake can only move in one direction at once and keeps direction on no input
            if(sensor.get_value('gravity')['y'] > 1):
                direction = "D"
            elif(sensor.get_value('gravity')['y'] < -1):
                direction = "U"
            elif(sensor.get_value('gravity')['x'] > 1):
                direction = "L"
            elif(sensor.get_value('gravity')['x'] < -1):
                direction = "R"
            
        if direction == "D":
            head.y -= SQUARE_SIZE
        elif direction == "U":
            head.y  += SQUARE_SIZE
        elif direction == "L":
            head.x -= SQUARE_SIZE
        elif direction == "R":
            head.x += SQUARE_SIZE

        #collisions
        #wall
        if(head.x < 0 or head.x == WINDOW_WIDTH or head.y < 0 or head.y == WINDOW_HEIGHT):
            end = True

        #body parts
        for i in range(len(segments)):
            if (head.x == segments[i][0] and head.y == segments[i][1]):
                end = True

        #end snake movement and show Game Over + Score
        if end:
            label = pyglet.text.Label(f'Game Over!  Score: {score}',
                            font_name='Pixel Game',
                            font_size=36,
                            x=10, y=10)
            label.draw()
        else:
            #draw head if it didn't collide with anything
            head.draw()  
        
    #draw the window contents/move once every second
    time.sleep(1)
            


pyglet.app.run()

#TODO
#boundaries (modulo or end?)
#end conditions
#end screen
#food appearance
#food consumption

#FIXME
#boundaries
#head can overtake body (direction change weird?)
#positioning of body parts?

