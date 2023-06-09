import note_mappings
from time import sleep
from tof import get_distance, close_sensors
from instrument import play, get_selected_instrument

UPDATE_HZ = 100
BURST_INSTRUMENTS = [  # Instruments that we do not need to stop playing when we change notes
    "Acid SQ Neutral.sf2",
    "Piano.sf2"
]
NUM_SENSORS = 3

get_note_name = note_mappings.get_note_name
octave_notes = note_mappings.octave_notes

active_notes = {
    # "C4": (stop_func, is_primed)
}

def noteBelongsToSensor(note: str, sensor_number):
    return note[0:-1] == octave_notes[sensor_number - 1]

while True:
    for sensor_number in range(1, NUM_SENSORS + 1):
        distance = get_distance(sensor_number)
        note = get_note_name(sensor_number, distance)
        selected_instrument = get_selected_instrument()

        if note in [
            note_mappings.RESPONSE_NOT_IN_PATH,
            note_mappings.RESPONSE_TOO_CLOSE,
            note_mappings.RESPONSE_TOO_FAR
        ]:
            for tup in active_notes.copy().items():
                active_note = tup[0]

                # We only want the notes this sensor is responsible for
                if not noteBelongsToSensor(active_note, sensor_number):
                    continue

                if selected_instrument not in BURST_INSTRUMENTS and active_notes[active_note][0]:
                    active_notes[active_note][0]()
                    del active_notes[active_note]
                else:
                    active_notes[active_note] = (None, False)
        elif note == note_mappings.RESPONSE_IN_SPACING:
            continue
        else:
            for tup in active_notes.copy().items():
                active_note = tup[0]

                # We only want the notes this sensor is responsible for
                if not noteBelongsToSensor(active_note, sensor_number):
                    continue

                # If the note is not the one we want to play, stop it
                if active_note != note:
                    stop_func, is_primed = active_notes.get(active_note, (None, False))

                    if selected_instrument in BURST_INSTRUMENTS:
                        active_notes[active_note] = (stop_func, False)
                    else:
                        stop_func()
                        del active_notes[active_note]

            stop_func, is_primed = active_notes.get(note, (None, False))

            if note not in active_notes or (selected_instrument in BURST_INSTRUMENTS and not is_primed):
                print("Playing note", note, distance, "cm")
                active_notes[note] = (play(selected_instrument, note), True)

    sleep(1 / UPDATE_HZ)