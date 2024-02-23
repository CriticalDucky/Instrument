from control_panel_data import get_data

OCTAVE_NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTE_MIDI_MAPPING = {note: midi for midi, note in enumerate(OCTAVE_NOTES)}

BURST_INSTRUMENTS = [  # Instruments that we do not need to stop playing when we change notes
    "Acid SQ Neutral.sf2",
    "Acid SQ Neutral",
    "Piano.sf2"
    "Piano"
]

# This function converts a note name to a MIDI note number
def note_to_midi(note: str):
    # Define the mapping of note names to MIDI note numbers
    

    # Extract the note name and octave from the input string
    note = note.upper()
    note_name = note[:-1]
    octave = int(note[-1])

    # Calculate the MIDI note number
    midi_note = NOTE_MIDI_MAPPING[note_name] + octave * 12 + 12

    return midi_note

def midi_to_note(midi_note: int):
    # Calculate the octave and note name
    octave = midi_note // 12 - 1
    note_name = list(NOTE_MIDI_MAPPING.keys())[list(NOTE_MIDI_MAPPING.values()).index(midi_note % 12)]

    # Return the note name and octave as a string
    return note_name + str(octave)

def sensor_to_note(sensor_number: int): # sensor_number: 1-12
    return OCTAVE_NOTES[sensor_number - 1]

def note_to_sensor(note: str): # note: C4, C#4, D4, D#4, E4, F4, F#4, G4, G#4, A4, A#4, B4
    note_without_octave = note[:-1]
    return OCTAVE_NOTES.index(note_without_octave) + 1

def create_chord(note: str, chord_type: str, inversion=0): # chord_type: major, minor; inversion: 0, 1, 2
    midi_num = note_to_midi(note)
    midi_table = [midi_num, midi_num + 4, midi_num + 7]

    if chord_type == 'Minor':
        midi_table[1] -= 1

    if inversion == 1:
        midi_table[0] += 12
    elif inversion == 2:
        midi_table[0] += 12
        midi_table[1] += 12

    return [midi_to_note(midi) for midi in midi_table]

# This function returns an ordered array of instruments as seen in the sounds folder.
# Structure: [
#   {'name': 'Acid SQ Neutral', 'path': 'this is the path to the soundfont file'},
#   {'name': 'Piano', 'path': 'this is the path to the soundfont file'},
#   ...
# ]
def get_libraries():
    import os

    # Path to the sounds folder
    script_dir = os.path.dirname(os.path.realpath(__file__))
    sounds_folder = os.path.join(script_dir, '..', 'sounds')

    # Initialize an empty dictionary to store library instrument information
    # The dictionary key is the name of the folder the file is in, and the value is a table with the file name and the full path to the file
    libraries = {}

    # Iterate through all files in the sounds folder
    for root, _, files in os.walk(sounds_folder):
        for file in files:
            # Check if the file is a soundfont file (.sf2)
            if file.endswith(".sf2") or file.endswith(".SF2"):
                # Extract instrument name from the file name (remove the ".sf2" extension)
                instrument_name = os.path.splitext(file)[0]
                
                # Get the full path to the soundfont file
                instrument_path = os.path.join(root, file)

                # Create a dictionary with instrument information and append it to the list
                instrument_info = {'name': instrument_name, 'path': instrument_path}
                
                # Get the name of the folder the file is in
                folder_name = os.path.basename(root)

                # Add the instrument to the list of instruments in the corresponding library
                if folder_name in libraries:
                    libraries[folder_name].append(instrument_info)
                else:
                    libraries[folder_name] = [instrument_info]

                

    # Return the list of instruments

    # instruments = sorted(instruments, key=lambda x: x['name'])
                    
    # sort the instruments in each library
    for library in libraries:
        libraries[library] = sorted(libraries[library], key=lambda x: x['name'])

    return libraries

            
def get_selected_instrument():
    return get_data('instrument')

def get_selected_octave():
    return get_data('octave')

def get_selected_chord():
    return get_data('chord')

def get_selected_inversion():
    return get_data('inversion')

def is_instrument_burst(instrument: str):
    return instrument in BURST_INSTRUMENTS