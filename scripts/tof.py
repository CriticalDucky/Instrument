import json
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)
cached_data_cm = [0] * 12

def get_data():
    data = ser.readline().decode().strip()
    if data:
        print("Received data:", data)

        global cached_data_cm
        cached_data_cm = json.loads(data)

    return cached_data_cm

def get_distance(sensor_number):
    distance_cm = get_data()[sensor_number - 1]

    if distance_cm < 700 and distance_cm > 0:
        print("Sensor", sensor_number, "distance", distance_cm, "cm")

    if distance_cm <= 0:
        print("Waiting for sensor data", sensor_number)

    return distance_cm  # cm
