import socket
import time
import math
import random



IP = '127.0.0.1'
PORT = 5700

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

counter = 0
button_1 = random.randint(0,1)

#probability that the button stays pressed/released in a time interval
#because it is unrealistic that it is pressed/released every 0.1s
p_stay = 0.9 

#send simulated button and accelerometer data in json format
while True:
    #simulate phone lying on the table
    #from testing: approx. x, y, z = (0.005, 0.01), (0.015,0.02), (1.0015, 1.0035)
    #factor 42 added to see changes happening in the 0.1s Intervals
    x = 0.0025 * math.sin(counter * 42) + 0.0075
    y = 0.0025 * math.sin(counter * 42) + 0.0175
    z = 0.001 * math.sin(counter * 42) + 1.0025

    if random.random() > p_stay:
        button_1 = 1 - button_1 #0->1 or 1 -> 0

    message = '{"button_1": ' + str(button_1) + ', "accelerometer" : {"x": ' + str(x) +  ', "y": ' + str(y) + ', "z": ' + str(z) + '}}'

    sock.sendto(message.encode(), (IP, PORT))

    #sanity check
    print(message)

    counter += 1
    time.sleep(0.1)