from DIPPID import SensorUDP

#FIXME check code/values with demo_device/demo_polling

# use UPD (via WiFi) for communication
PORT = 5700
sensor = SensorUDP(PORT)

def handle_accelerometer_x(data):
    print(f"accelerometer x value: {data}")

def handle_accelerometer_y(data):
    print(f"accelerometer y value: {data}")

def handle_accelerometer_z(data):
    print(f"accelerometer z value: {data}")

def handle_button_1(data):
    if data == 1:
        print("button 1 pressed")
    else:
        print("button 1 not pressed")

sensor.register_callback('accelerometer_x', handle_accelerometer_x)
sensor.register_callback('accelerometer_y', handle_accelerometer_y)
sensor.register_callback('accelerometer_z', handle_accelerometer_z)
sensor.register_callback('button_1', handle_button_1)
