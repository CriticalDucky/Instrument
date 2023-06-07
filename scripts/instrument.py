from time import sleep
import fluidsynth

def note_to_midi(note):
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

def findsf2file(name):
    import os
    for root, _, files in os.walk("sounds"):
        for file in files:
            if file.endswith(".sf2") and file.startswith(name):
                return os.path.join(root, file)

fs = fluidsynth.Synth()
fs.start()

def play(instrument = "Acid SQ Neutral.sf2", note = "C4"):
    midi = note_to_midi(note)
    sfid = fs.sfload(findsf2file(instrument))
    fs.program_select(0, sfid, 0, 0)

    fs.noteon(0, midi, 127)
    
    def stop(secondsUntilStop = 0):
        sleep(secondsUntilStop)
        fs.noteoff(0, midi) 

    return stop

