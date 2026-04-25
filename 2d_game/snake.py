import pyglet
from pyglet import window, shapes
from DIPPID import SensorUDP
import random
import time

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PORT = 5700
SQUARE_SIZE = 20

sensor = SensorUDP(PORT)

win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)

#initial values
score = 0
direction = "R" #one of "R", "L", "U", "D"
end = False

#shapes
head = shapes.Rectangle(400, 400, SQUARE_SIZE, SQUARE_SIZE, (0, 100, 50))
body = shapes.Rectangle(400, 400, SQUARE_SIZE, SQUARE_SIZE, (0, 150, 100))
food = shapes.Rectangle(random.randint(0, (WINDOW_WIDTH - SQUARE_SIZE)), random.randint(0, (WINDOW_HEIGHT - SQUARE_SIZE)), SQUARE_SIZE, SQUARE_SIZE, (200, 0, 0))
endscreen = ...#FIXME

#coordinated of body segments
#FIXME should be empty at the start, just for testing
segments = [[420, 400], [440, 400], [460, 400]]


#play
@win.event
def on_draw():
    #global variables we want to use in this function
    global direction
    global segments
    #FIXME add some?

    win.clear()
    # check if sensor data is received
    if(not sensor.get_capabilities() == [] and not end):
        #update body positions: #TODO test
        #each takes the position of the one in front, the first takes the position of the head
        print(f"segments: {segments}")#FIXME error with assignments
        for i in range(len(segments)-1, 0, -1):
            print(i)
            temp = segments[i-1]
            segments[i] = temp #FIXME
            body.x = segments[i][0]
            body.y = segments[i][1]
            body.draw()
            print(f"b{i}({body.x},{body.y})")#FIXME
            print(f"segments: {segments}")#FIXME
        if not segments == []:
            segments[0][0] = head.x
            segments[0][1] = head.y
            body.x = head.x
            body.y = head.y
            body.draw()
            print(f"b0({body.x},{body.y})")#FIXME
            print(f"segments: {segments}")#FIXME why is b1 changed here?????



        #Threshold for smooter operation
        #snake can only move in one direction at once and keeps direction on no input
        if(sensor.get_value('gravity')['y'] > 1):
            direction = "U"
        elif(sensor.get_value('gravity')['y'] < -1):
            direction = "D"
        elif(sensor.get_value('gravity')['x'] > 1):
            direction = "R"
        elif(sensor.get_value('gravity')['x'] < -1):
            direction = "L"
        
    if direction == "U":
        head.y -= SQUARE_SIZE
    elif direction == "D":
        head.y  += SQUARE_SIZE
    elif direction == "R":
        head.x -= SQUARE_SIZE
    elif direction == "L":
        head.x += SQUARE_SIZE

    print(f"h({head.x},{head.y})") #FIXME
    head.draw()

    if end:
        endscreen.draw()
    
    #move every second
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

