import socket
import time
import math
import random


def accelerometer():

    IP = '127.0.0.1'
    PORT = 5700

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    counter = 0

    while True:
        #send simulated accelerometer data in json format
        
        #FIXME for some reason if I send anything other than a number as value for accelerometer, nothing is received
        #accelerometer = {"x":math.sin(counter), "y":math.sin(counter/2), "z":math.sin(counter*2) }
        #message = '{"accelerometer" : ' + str(accelerometer) + '}'
        
        x = '{"accelerometer_x" : ' + str(math.sin(counter)) + '}'
        y = '{"accelerometer_y" : ' + str(math.sin(counter/2)) + '}'
        z = '{"accelerometer_z" : ' + str(math.sin(counter*2)) + '}'

        #send simulated button data in json format (1 for button pressed, 0 for button not pressed)
        button_1 = '{"button_1" : ' + str(random.randint(0,1)) + '}'

        sock.sendto(x.encode(), (IP, PORT))
        sock.sendto(y.encode(), (IP, PORT))
        sock.sendto(z.encode(), (IP, PORT))
        sock.sendto(button_1.encode(), (IP, PORT))

        #sanity check
        print(f"x: {x}, y: {y}, z: {z}, button 1: {button_1}")

        counter += 1
        time.sleep(1)



# def accelerometer():
#     IP = '127.0.0.1'
#     PORT = 5700

#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     counter = 0
#     while True:
#         accelerometer = {"x":math.sin(counter), "y":math.sin(counter/2), "z":math.sin(counter*2) }
#         message = '{"accelerometer" : ' + str(accelerometer) + '}'
#         #FIXME
#         message = '{"accelerometer" : ' + str("test") + '}'
#         print(message)#FIXME

#         sock.sendto(message.encode(), (IP, PORT))
#         counter += 1
#         time.sleep(0.1)
#         #FIXME
#         if counter == 10:
#             break

accelerometer()



