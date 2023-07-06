'''
Module for mapping tof sensor readings to notes
'''
BASELINE_DISTANCE = 5 # cm; distance from sensor to first octave
OCTAVE_SPAN_SIZE = 4 # cm; size of activation area of each octave
OCTAVE_SPACING = 4 # cm; distance between octaves
FINGER_WIDTH_HALF = 1.5/2 # cm; width of finger divided by 2

RESPONSE_TOO_CLOSE = "rTC"
RESPONSE_TOO_FAR = "rTF"
RESPONSE_NOT_IN_PATH = "rNP"
RESPONSE_IN_SPACING = "rIP"

octave_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
num_octaves = 7

def get_note_name(sensor_number, distance):
    distance += FINGER_WIDTH_HALF

    if distance < BASELINE_DISTANCE:
        return RESPONSE_TOO_CLOSE
    
    distance -= BASELINE_DISTANCE
    area_group_size = OCTAVE_SPAN_SIZE + OCTAVE_SPACING
    octave = int(distance // area_group_size)
    
    if distance % area_group_size > OCTAVE_SPAN_SIZE:
        if octave == num_octaves:
            return RESPONSE_TOO_FAR

        return RESPONSE_IN_SPACING

    if octave > num_octaves:
        return RESPONSE_TOO_FAR

    note = octave_notes[(sensor_number - 1)]
    return note + str(octave)