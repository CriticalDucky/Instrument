from control_panel_data import get_data

# This function converts a note name to a MIDI note number
def note_to_midi(note: str):
    # Define the mapping of note names to MIDI note numbers
    note_mapping = {
        'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3,
        'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8,
        'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11
    }

    # Extract the note name and octave from the input string
    note = note.upper()
    note_name = note[:-1]
    octave = int(note[-1])

    # Calculate the MIDI note number
    midi_note = note_mapping[note_name] + octave * 12 + 12

    return midi_note
            
# This function returns an ordered array of instruments as seen in the sounds folder.
# Structure: [
#   {'name': 'Acid SQ Neutral', 'path': 'this is the path to the soundfont file'},
#   {'name': 'Piano', 'path': 'this is the path to the soundfont file'},
#   ...
# ]
def get_all_instruments():
    import os

    # Path to the sounds folder
    sounds_folder = "sounds"

    # Initialize an empty list to store instrument information
    instruments = []

    # Iterate through all files in the sounds folder
    for root, _, files in os.walk(sounds_folder):
        for file in files:
            # Check if the file is a soundfont file (.sf2)
            if file.endswith(".sf2"):
                # Extract instrument name from the file name (remove the ".sf2" extension)
                instrument_name = os.path.splitext(file)[0]
                
                # Get the full path to the soundfont file
                instrument_path = os.path.join(root, file)

                # Create a dictionary with instrument information and append it to the list
                instrument_info = {'name': instrument_name, 'path': instrument_path}
                instruments.append(instrument_info)

    # Return the list of instruments
    return instruments

            
def get_selected_instrument():
    return get_data('instrument')

def get_selected_octave():
    return get_data('octave')