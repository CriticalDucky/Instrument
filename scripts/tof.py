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
        data = ser.readline().decode().strip()[1:-1]
        if data:
            data = data.split()
            data = [float(x) for x in data]

            print(data)

            global cached_data_cm

            for idx, val in enumerate(data):
                cached_data_cm[idx] = val

        

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

new_thread = threading.Thread(target=get_data)
new_thread.start()
