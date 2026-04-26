'''
##########################################################################################
    Y
  .-^-.
 /     \      .- ~ ~ -.
()     ()    /   _ _   `.                     _ _ _
 \_   _/    /  /     \   \                . ~  _ _  ~ .
   | |     /  /       \   \             .' .~       ~-. `.
   | |    /  /         )   )           /  /             `.`.
   \ \_ _/  /         /   /           /  /                `'
    \_ _ _.'         /   /           (  (
                    /   /             \  \
                   /   /               \  \
                  /   /                 )  )
                 (   (                 /  /
                  `.  `.             .'  /
                    `.   ~ - - - - ~   .'
                       ~ . _ _ _ _ . ~


https://www.asciiart.eu/art/b12656730a00300c
##########################################################################################
How to play:
1. Start the DIPPID app on your phone, set it to your_ip:5700 and start sending data
2. Hold your phone horizontal with the short side pointing to the front.
3. Start this script
4. Tilt your phone to the front/back or to the sides to change the direction of the snake.
5. Have fun!
##########################################################################################
'''

import pyglet
from pyglet import window, shapes, font
from DIPPID import SensorUDP
import random
import time
import sys

#window height/width have to be multiples of the square size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PORT = 5700
SQUARE_SIZE = 20

#delay between snake movements. Decrease to increase the speed
delay = 0.25

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
#food position has to be in the window and a multiple of SQUARE_SIZE, so the snake head can match the position
food = shapes.Rectangle(random.randint(0, int((WINDOW_WIDTH - SQUARE_SIZE)/SQUARE_SIZE)) * SQUARE_SIZE, random.randint(0, int((WINDOW_HEIGHT - SQUARE_SIZE)/SQUARE_SIZE)) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE, (200, 0, 0))

#coordinated of body segments
segments = [[380, 400], [360, 400], [340, 400]] #inital snake body

#get position for the next food that is not occupied by the snake
def get_new_food_position():
    x = random.randint(0, int((WINDOW_WIDTH - SQUARE_SIZE)/SQUARE_SIZE)) * SQUARE_SIZE
    y = random.randint(0, int((WINDOW_HEIGHT - SQUARE_SIZE)/SQUARE_SIZE)) * SQUARE_SIZE

    #check head
    if (head.x == x and head.y == y):
        return(get_new_food_position())
    else:
        #check body
        for i in range(len(segments)):
            if (segments[i][0] == x and segments[i][1] == y):
                return(get_new_food_position())
        print(f"food position: {x},{y}") #FIXME testing
        return(x, y) #no collision detected until here

#add new body segment at the end of the snake
def add_body_segment():
    if segments == []:
        prevx = head.x
        prevy = head.y
    else:
        prevx = body.x
        prevy = body.y
    
    x = prevx
    y = prevy
    
    if direction == "D":
        y = prevy + SQUARE_SIZE 
    elif direction == "U":
        y = prevy - SQUARE_SIZE
    elif direction == "L":
        x = prevx + SQUARE_SIZE
    elif direction == "R":
        x = prevx - SQUARE_SIZE

    segments.append([x,y])

    

#play
@win.event
def on_draw():
    #global variables we want to use in this function
    global direction
    global segments
    global score
    global end
    global delay

    if not end:

        win.clear()

        food.draw()

        #update body positions:
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
            #check if the movement is the one from before so we don't accidentally overwrite the next movement
            #in case the user does not tilt the device back to horizontal 

            #people kept intuitively tilting the phone to the back and running into themselves.
            #adjusted y threshold accordingly 
            if(sensor.get_value('gravity')['y'] > 5 and not direction == "D"):
                
                direction = "D"
            if(sensor.get_value('gravity')['y'] < -2 and not direction == "U"):
                direction = "U"
            if(sensor.get_value('gravity')['x'] > 2 and not direction == "L"):
                direction = "L"
            if(sensor.get_value('gravity')['x'] < -2 and not direction == "R"):
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
        #food
        if(head.x == food.x and head.y == food.y):
            score += 1
            food.x, food.y = get_new_food_position()
            add_body_segment()
            

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
    time.sleep(delay)

pyglet.app.run()

#TODO:
#add play again button
#?fix weird warning bc of ascii art?
