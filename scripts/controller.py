from note_mappings import get_note_name
from time import sleep
from ultrasonic import get_distance
from instrument import play, get_selected_instrument

UPDATE_INTERVAL = 0.05 # 20 Hz
BURST_INSTRUMENTS = [ # Instruments that we do not need to stop playing when we change notes
    "Acid SQ Neutral",
]
NUM_SENSORS = 1

active_notes = {
    # "C4": (stop_func, is_prime)
}

while True:
    for sensor_number in range(1, NUM_SENSORS + 1):
        distance = get_distance(sensor_number)
        note = get_note_name(sensor_number, distance)
        selected_instrument = get_selected_instrument()

        if note is None and note not in BURST_INSTRUMENTS:
            stop = active_notes.get(note)

            if stop:
                stop()
                del active_notes[note]
            
            continue

        if note not in active_notes or selected_instrument in BURST_INSTRUMENTS:
            print("Playing note", note)
            active_notes[note] = play(selected_instrument, note)

    sleep(UPDATE_INTERVAL)