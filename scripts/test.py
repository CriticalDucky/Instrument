import instrument
from time import sleep

melody = [
('G5', 250), ('G5', 250), ('E5', 250), ('F5', 250), ('G5', 250),
('D5', 250), ('F5', 250), ('G5', 250), ('B4', 250),
('D5', 250), ('G4', 250), ('D5', 250), ('G4', 250),
('E3', 250), ('B3', 250), ('D4', 250), ('B3', 250),
('G5', 250), ('G5', 250), ('E5', 250), ('C#5', 250), ('F5', 250), ('E5', 250), ('D5', 250), ('D5', 250),
('D4', 250), ('G4', 250), ('C5', 250), ('B4', 250),
('C3', 250), ('B3', 250), ('B2', 250)
]

for note, duration in melody:
    stop = instrument.play(note = note, instrument="Piano.sf2")
    sleep(duration / 1000)
    stop()