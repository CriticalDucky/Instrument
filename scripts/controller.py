import note_mappings
from time import sleep
from tof import get_distance
from instrument import play, get_selected_instrument
import matplotlib.pyplot as plt
import numpy as np

UPDATE_INTERVAL = 0.01  # 100 Hz
BURST_INSTRUMENTS = [  # Instruments that we do not need to stop playing when we change notes
    "Acid SQ Neutral.sf2",
]
NUM_SENSORS = 1

get_note_name = note_mappings.get_note_name
octave_notes = note_mappings.octave_notes

active_notes = {
    # "C4": (stop_func, is_primed)
}

history_length = 50  # Number of past measurements to display
history = np.zeros(history_length)  # Initialize an array to store the distance history

plt.figure()
ax = plt.axes()
ax.set_xlim([-history_length, 0])
ax.set_ylim([0, 50])  # Adjust the y-axis limits as needed

bars = ax.bar(np.arange(-history_length, 0), history)  # Create an initial set of empty bars
plt.show(block=False)  # Set block=False to allow non-blocking plotting

def update_graph():
    # Read the distance measurement from your VL53L0X sensor
    distance = get_distance(1)

    # Shift the distance history array to the left and append the new measurement
    distance_history = np.roll(history, -1)
    distance_history[-1] = distance

    # Update the heights of the bars to reflect the new distance measurements
    for bar, dist in zip(bars, distance_history):
        bar.set_height(dist)

    plt.pause(0.01)

while True:
    for sensor_number in range(1, NUM_SENSORS + 1):
        distance = get_distance(sensor_number)
        note = get_note_name(sensor_number, distance)
        selected_instrument = get_selected_instrument()
        stop_func, is_primed = active_notes.get(note, (None, False))

        if note in [
            note_mappings.RESPONSE_NOT_IN_PATH,
            note_mappings.RESPONSE_TOO_CLOSE,
            note_mappings.RESPONSE_TOO_FAR
        ] and selected_instrument not in BURST_INSTRUMENTS:
            if stop_func:
                stop_func()
                del active_notes[note]

            continue
        elif note in [
            note_mappings.RESPONSE_NOT_IN_PATH,
            note_mappings.RESPONSE_TOO_CLOSE,
            note_mappings.RESPONSE_TOO_FAR
        ]:
            for tup in active_notes.copy().items():
                active_note = tup[0]

                # We only want the notes this sensor is responsible for
                if not active_note.startswith(octave_notes[sensor_number - 1]):
                    continue

                active_notes[active_note] = (None, False)
        elif note == note_mappings.RESPONSE_IN_SPACING:
            print("In spacing")
            continue
        else:
            for tup in active_notes.copy().items():
                active_note = tup[0]

                # We only want the notes this sensor is responsible for
                if not active_note.startswith(octave_notes[sensor_number - 1]):
                    continue

                if active_note != note:
                    active_notes[active_note] = (stop_func, False)

            stop_func, is_primed = active_notes.get(note, (None, False))

            if note not in active_notes or (selected_instrument in BURST_INSTRUMENTS and not is_primed):
                print("Playing note", note, distance, "cm")
                active_notes[note] = (play(selected_instrument, note), True)

    update_graph()
    # sleep(UPDATE_INTERVAL)
