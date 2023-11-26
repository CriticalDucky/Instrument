ACTIVATION_ZONE = 20 # cm

import serial
import serial.tools.list_ports
import threading

def find_serial_port(device_name):
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if device_name in port.device:
            print("Found", device_name, "at", port.device)
            return port.device
    return None

device_name = "ttyACM"  # Adjust this to match your device name
serial_port = find_serial_port(device_name)
    
ser = serial.Serial(serial_port, 9600)
cached_data_cm = [0] * 12

def get_data():
    while True:
        data = None

        try:
            data = ser.readline().decode().strip()
            if data:
                data1 = data.split()
                # print(data)
                data1 = [float(x)/10 for x in data1]

                global cached_data_cm

                for idx, val in enumerate(data1):
                    cached_data_cm[idx] = val
        except:
            if data:
                print("The pico has something to say!", data)
    

def get_distance(sensor_number):
    if not serial_port:
        print(f"{device_name}X not found")
        return 0

    distance_cm = cached_data_cm[sensor_number - 1]

    # if distance_cm < 700 and distance_cm > 0:
    #     print("Sensor", sensor_number, "distance", distance_cm, "cm")

    # if distance_cm <= 0:
    #     print("Waiting for sensor data", sensor_number)

    return distance_cm  # cm

def get_sensor_binaries(): # A table of 12 1s and 0s, 1 if the sensor has something within 20cm, 0 otherwise
    binaries = []

    for sensor_number in range(1, 13): # 12 sensors
        distance = get_distance(sensor_number)
        
        if distance < ACTIVATION_ZONE and distance > 0:
            binaries.append(1)
        else:
            binaries.append(0)

    print(cached_data_cm)

    return binaries

new_thread = threading.Thread(target=get_data)
new_thread.start()