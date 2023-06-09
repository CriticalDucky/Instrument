import instrument
from time import sleep

melody = [('C4', 500), ('C4', 500), ('G4', 500), ('G4', 500), ('A4', 500), ('A4', 500), ('G4', 1000), ('F4', 500), ('F4', 500), ('E4', 500), ('E4', 500), ('D4', 500), ('D4', 500), ('C4', 1000)]

for note, duration in melody:
    stop = instrument.play(note = note, instrument="Analog Saw.sf2")
    sleep(duration / 1000)
    stop()