from scripts.data.control_panel_data import get_data

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

'''
[
    {
        'name': 'Library 1',
        'data': [
            {'name': 'Instrument 1', 'path': 'path/to/instrument1.sf2'},
            {'name': 'Instrument 2', 'path': 'path/to/instrument2.sf2'},
            ...
        ]
    },
    {
        'name': 'Library 2',
        'data': [
            {'name': 'Instrument 1', 'path': 'path/to/instrument1.sf2'},
            {'name': 'Instrument 2', 'path': 'path/to/instrument2.sf2'},
            ...
        ]
    },
    ...
]
'''
def get_libraries():
    import os

    # Path to the sounds folder
    script_dir = os.path.dirname(os.path.realpath(__file__))
    sounds_folder = os.path.join(script_dir, '..', 'sounds')

    # Initialize an empty list to store library instrument information
    # Each item in the list is a dictionary containing the library name and instrument data
    libraries = []

    # Iterate through all files in the sounds folder
    for root, _, files in os.walk(sounds_folder):
        for file in files:
            # Check if the file is a soundfont file (.sf2)
            if file.endswith(".sf2") or file.endswith(".SF2"):
                # Extract instrument name from the file name (remove the ".sf2" extension)
                instrument_name = os.path.splitext(file)[0]
                
                # Get the full path to the soundfont file
                instrument_path = os.path.join(root, file)

                # Create a dictionary with instrument information
                instrument_info = {'name': instrument_name, 'path': instrument_path}
                
                # Get the name of the folder the file is in
                folder_name = os.path.basename(root)

                # Check if the library already exists in the list
                existing_library = next((item for item in libraries if item['name'] == folder_name), None)
                if existing_library:
                    existing_library['data'].append(instrument_info)
                else:
                    # Create a new library entry
                    libraries.append({'name': folder_name, 'data': [instrument_info]})

                

    # Return the list of instruments

    # instruments = sorted(instruments, key=lambda x: x['name'])
                    
    # # sort the instruments in each library
    # for library in libraries:
    #     libraries[library] = sorted(libraries[library], key=lambda x: x['name'])

    return libraries

            
def get_selected_library():
    return get_data('library')

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