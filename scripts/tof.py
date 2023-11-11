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
past_binaries = [0] * 12

def get_data():
    while True:
        data = None

        try:
            data = ser.readline().decode().strip()
            if data:
                data1 = data.split()
                print(data)
                data1 = [float(x)/10 for x in data1]

                global cached_data_cm

                for idx, val in enumerate(data1):
                    cached_data_cm[idx] = val
        except:
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
        distance_opp = get_distance((sensor_number + 6) % 12)
        
        if distance_opp < 800 and distance < ACTIVATION_ZONE:
            binaries.append(1)
        else:
            binaries.append(0)

    global past_binaries # We use the past data to correct the current data

    old_binaries = binaries.copy()

    for idx, val in enumerate(old_binaries): # Sometimes the sensors are not accurate, so we use the past data to correct them
        if past_binaries[idx] == 1 and val == 0:
            binaries[idx] = 1

    past_binaries = old_binaries # Update the past data

    return binaries

new_thread = threading.Thread(target=get_data)
new_thread.start()