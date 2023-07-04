'''
Module for mapping tof sensor readings to notes
'''
BASELINE_DISTANCE = 5 # cm
NOTE_DISTANCE = 8 # cm

octave_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
num_octaves = 7

# The note depends on the sensor number (1-12), and the octave depends on the distance (cm)
# The distance is mapped to an octave, and the sensor number is mapped to a note in that octave
# Octaves are separated by 4 cm.
def get_note_name(sensor_number, distance):
    if distance < BASELINE_DISTANCE:
        return None

    octave = int((distance - BASELINE_DISTANCE) // NOTE_DISTANCE)

    if octave > num_octaves:
        return None

    note = octave_notes[(sensor_number - 1)]
    return note + str(octave)