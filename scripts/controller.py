from note_mappings import get_note_name, octave_notes
from time import sleep
from ultrasonic import get_distance
from instrument import play, get_selected_instrument

UPDATE_INTERVAL = 0.05 # 20 Hz
BURST_INSTRUMENTS = [ # Instruments that we do not need to stop playing when we change notes
    "Acid SQ Neutral.sf2",
]
NUM_SENSORS = 1

active_notes = {
    # "C4": (stop_func, is_primed)
}

while True:
    for sensor_number in range(1, NUM_SENSORS + 1):
        distance = get_distance(sensor_number)
        note = get_note_name(sensor_number, distance)
        selected_instrument = get_selected_instrument()
        stop_func, is_primed = active_notes.get(note, (None, False))

        if note is None and selected_instrument not in BURST_INSTRUMENTS:
            if stop_func:
                stop_func()
                del active_notes[note]
            
            continue
        elif note is None:
            for tup in active_notes.copy().items():
                active_note = tup[0]

                if not active_note.startswith(octave_notes[sensor_number - 1]): # We only want the notes this sensor is responsible for
                    continue

                active_notes[active_note] = (None, False)
        else:
            for tup in active_notes.copy().items():
                active_note = tup[0]

                if not active_note.startswith(octave_notes[sensor_number - 1]): # We only want the notes this sensor is responsible for
                    continue

                if active_note != note:
                    active_notes[active_note] = (stop_func, False)

            stop_func, is_primed = active_notes.get(note, (None, False))

            if note not in active_notes or (selected_instrument in BURST_INSTRUMENTS and not is_primed):
                print("Playing note", note)
                active_notes[note] = (play(selected_instrument, note), True)

    sleep(UPDATE_INTERVAL)