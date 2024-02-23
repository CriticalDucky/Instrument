from time import sleep
from instrument_util import note_to_midi, get_libraries
import fluidsynth
import platform

fs = fluidsynth.Synth()

isRaspberryPi = platform.system() == "Linux" and (platform.machine() == "armv7l" or platform.machine() == "aarch64")
print(platform.system(), platform.machine(), isRaspberryPi)
if isRaspberryPi:
    fs.start(driver="alsa")
else:
    print("You are not on a Raspberry Pi.")
    fs.start()

def play(library: int, instrument: int, note = "C4"):
    midi = note_to_midi(note)
    file = get_libraries()[library][instrument]['path']

    if file is None:
        raise Exception("Could not find soundfont file for instrument " + instrument)

    sfid = fs.sfload(file)
    fs.program_select(0, sfid, 0, 0)

    fs.noteon(0, midi, 127)
    print("Playing", note, "on", instrument)
    
    def stop(secondsUntilStop=0):
        if secondsUntilStop: sleep(secondsUntilStop)
        fs.noteoff(0, midi)

    return stop