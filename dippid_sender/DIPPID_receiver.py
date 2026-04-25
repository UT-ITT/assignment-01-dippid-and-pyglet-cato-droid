from DIPPID import SensorUDP

# use UPD (via WiFi) for communication
PORT = 5700
sensor = SensorUDP(PORT)

def handle_accelerometer(data):
    print(f"accelerometer data: {data}")

#note: this will not print something as often as the accelerometer,
#because callback functions are only called when the value changes
#so we get notified when the button is newly pressed/released,
#but not when it is continously pressed/not pressed
def handle_button_1(data):
    if data == 1:
        print("button 1 pressed")
    else:
        print("button 1 released")

sensor.register_callback('accelerometer', handle_accelerometer)
sensor.register_callback('button_1', handle_button_1)
