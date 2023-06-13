from time import sleep
import fluidsynth
import platform

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

def find_sf2_file(name):
    import os
    for root, _, files in os.walk("sounds"):
        for file in files:
            if file.endswith(".sf2") and file.startswith(name):
                return os.path.join(root, file)

fs = fluidsynth.Synth()

isRaspberryPi = platform.system() == "Linux" and platform.machine() == "armv7l"
print(platform.system(), platform.machine(), isRaspberryPi)
if isRaspberryPi:
    fs.start(driver="alsa")
else:
    fs.start()

def play(instrument = "Acid SQ Neutral.sf2", note = "C4"):
    midi = note_to_midi(note)
    file = find_sf2_file(instrument)

    if file is None:
        raise Exception("Could not find soundfont file for instrument " + instrument)

    sfid = fs.sfload(file)
    fs.program_select(0, sfid, 0, 0)

    fs.noteon(0, midi, 127)
    
    def stop(secondsUntilStop):
        if secondsUntilStop: sleep(secondsUntilStop)
        fs.noteoff(0, midi)

    return stop

def get_selected_instrument():
    return "Acid SQ Neutral.sf2"