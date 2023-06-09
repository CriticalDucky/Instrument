import instrument
from time import sleep

melody = [
('G5', 500), ('G5', 500), ('G5', 500), ('G5', 500), ('E5', 250), ('F5', 250), ('G5', 500), ('D5', 250), ('F5', 250), ('G5', 500),
('B4', 500), ('B4', 500), ('B4', 500), ('B4', 500), ('D4', 250), ('G4', 250), ('D4', 500), ('G4', 250), ('E4', 250), ('B4', 500),
('D4', 500), ('E4', 500), ('B3', 500), ('D4', 250), ('B3', 250)
]

for note, duration in melody:
    stop = instrument.play(note = note, instrument="Piano.sf2")
    sleep(duration / 1000)
    stop()