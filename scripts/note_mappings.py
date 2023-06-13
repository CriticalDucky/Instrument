'''
Module for mapping ultrasonic sensor readings to notes
'''

octave_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
num_octaves = 7

# The note depends on the sensor number (1-12), and the octave depends on the distance (cm)
# The distance is mapped to an octave, and the sensor number is mapped to a note in that octave
# Octaves are separated by 4 cm.
def get_note_name(sensor_number, distance):
    octave = (distance + 4) // 4

    if octave > num_octaves:
        return None

    note = octave_notes[(sensor_number - 1)]
    return note + str(octave)