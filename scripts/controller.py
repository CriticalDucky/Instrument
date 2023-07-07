import note_mappings
from time import sleep
from tof import get_distance
from instrument import play, get_selected_instrument
import matplotlib.pyplot as plt
import numpy as np

UPDATE_HZ = 300
BURST_INSTRUMENTS = [  # Instruments that we do not need to stop playing when we change notes
    "Acid SQ Neutral.sf2",
]
NUM_SENSORS = 1

get_note_name = note_mappings.get_note_name
octave_notes = note_mappings.octave_notes

active_notes = {
    # "C4": (stop_func, is_primed)
}

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

                print("Possibility 1")

            print("Possibility 2")

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
                print("This better not be printing 1")
        elif note == note_mappings.RESPONSE_IN_SPACING:
            print("In spacing")
            continue
        else:
            print("Possibility 4")

            for tup in active_notes.copy().items():
                active_note = tup[0]

                # We only want the notes this sensor is responsible for
                if not active_note.startswith(octave_notes[sensor_number - 1]):
                    continue

                if active_note != note:
                    print("This better not be printing 2")
                    active_notes[active_note] = (stop_func, False)

            stop_func, is_primed = active_notes.get(note, (None, False))

            if note not in active_notes or (selected_instrument in BURST_INSTRUMENTS and not is_primed):
                print("Playing note", note, distance, "cm")
                active_notes[note] = (play(selected_instrument, note), True)
                print("THIS SHOULD BE RUNNING!!!")

    sleep(1 / UPDATE_HZ)
