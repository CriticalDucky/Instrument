import instrument
from time import sleep

melody = [
('G4', 500), ('F4', 250), ('G4', 250), ('G4', 500), ('F4', 250), ('G4', 250), ('G4', 500), ('F4', 250), ('G4', 250),
('G4', 500), ('F4', 250), ('G4', 250), ('G4', 500), ('F4', 250), ('G4', 250),
('B4', 250), ('D5', 250), ('E5', 500), ('E5', 250), ('D5', 250), ('D5', 500),
('B4', 250), ('D5', 250), ('E5', 250), ('E5', 250), ('E5', 500)
]

for note, duration in melody:
    stop = instrument.play(note = note, instrument="Piano.sf2")
    sleep(duration / 1000)
    stop()