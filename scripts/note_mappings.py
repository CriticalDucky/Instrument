'''
Module for mapping tof sensor readings to notes
'''
BASELINE_DISTANCE = 4  # cm; distance from sensor to first octave
OCTAVE_SPAN_SIZE = 1  # cm; size of activation area of each octave
OCTAVE_SPACING = 3  # cm; distance between octaves
FINGER_WIDTH_HALF = 0#1.5/2  # cm; width of finger divided by 2
DIAMETER = BASELINE_DISTANCE * 2 + 7 * (OCTAVE_SPAN_SIZE + OCTAVE_SPACING)

'''
0 

1 

2    

3 

4  
    ██ 2
5  
    ░░
6  
    ░░
7  
    ░░ 2
8  
    ██ 3
9  
    ░░
10 
    ░░
11 
    ░░ 3
12 
    ██ 4
13 
    ░░
14 
    ░░
15 
    ░░ 4
16 
    ██ 5
17 
    ░░
18 
    ░░
19 
    ░░
20 
    ██ 6
21
    ░░
22
    ░░
23
    ░░ 6
24
    ██ 7
25
    ░░
26
    ░░
27
    ░░
28
   
29
   
30
   
31
   
32
'''

RESPONSE_TOO_CLOSE = "rTC"
RESPONSE_TOO_FAR = "rTF"
RESPONSE_NOT_IN_PATH = "rNP"
RESPONSE_IN_SPACING = "rIP"

octave_notes = ['C', 'C#', 'D', 'D#', 'E',
                'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
first_octave = 2
last_octave = 7


def get_note_name(sensor_number, distance):
    distance += FINGER_WIDTH_HALF

    if distance < BASELINE_DISTANCE:
        return RESPONSE_TOO_CLOSE

    distance -= BASELINE_DISTANCE
    area_group_size = OCTAVE_SPAN_SIZE + OCTAVE_SPACING
    octave = int(distance // area_group_size) + first_octave

    if (
            distance % area_group_size <= OCTAVE_SPACING and
            octave <= last_octave
        ) or (
            distance % area_group_size <= BASELINE_DISTANCE and
            octave == last_octave + 1
    ):
        return RESPONSE_IN_SPACING

    if octave > last_octave:
        return RESPONSE_TOO_FAR

    note = octave_notes[(sensor_number - 1)]
    return note + str(octave)
