from instrument import play, get_selected_instrument, get_selected_octave
from tof import get_sensor_binaries

BURST_INSTRUMENTS = [  # Instruments that we do not need to stop playing when we change notes
    "Acid SQ Neutral.sf2",
    "Piano.sf2"
]

octave_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

active_note_info = {
    # [1-12]: stop_func, called note_info in the code below
}

def loop():
    octave = get_selected_octave()
    binaries = get_sensor_binaries()
    selected_instrument = get_selected_instrument()
    isBurst = selected_instrument in BURST_INSTRUMENTS

    for idx, val in enumerate(binaries):
        sensor_number = idx + 1
        note_info = active_note_info.get(sensor_number, None) # stop_func

        if val == 1 and note_info is None:
            note = octave_notes[idx] + str(octave)

            stop_func = play(selected_instrument, note)
            active_note_info[sensor_number] = stop_func
        elif val == 0 and note_info is not None:
            if isBurst:
                active_note_info[sensor_number] = None
            else:
                note_info()