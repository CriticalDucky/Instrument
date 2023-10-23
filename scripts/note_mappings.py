'''
Module for mapping tof sensor readings to notes
'''
BASELINE_DISTANCE = 10  # cm; distance from sensor to first octave
OCTAVE_SPAN_SIZE = 10  # cm; size of activation area of each octave
OCTAVE_SPACING = 2  # cm; distance between octaves

RESPONSE_TOO_CLOSE = "rTC"
RESPONSE_TOO_FAR = "rTF"
RESPONSE_NOT_IN_PATH = "rNP"
RESPONSE_IN_SPACING = "rIP"

octave_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
octave = 4

def get_note_name(sensor_number, distance):
    if distance < BASELINE_DISTANCE:
        return RESPONSE_TOO_CLOSE

    distance -= BASELINE_DISTANCE

    if distance < OCTAVE_SPACING:
        return RESPONSE_IN_SPACING
    
    distance -= OCTAVE_SPACING

    if distance > (OCTAVE_SPAN_SIZE):
        return RESPONSE_TOO_FAR

    return octave_notes[(sensor_number - 1)] + str(octave)
