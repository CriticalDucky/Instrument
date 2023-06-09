import instrument
from time import sleep

melody = [
('E5', 250), ('F5', 250), ('D5', 250), ('E5', 250), ('E5', 250), ('F5', 250),
('D5', 500), ('A4', 250), ('A4', 250), ('D5', 500),
('D5', 250), ('E5', 250), ('E5', 250), ('F5', 250), ('D5', 250), ('E5', 250),
('C5', 500), ('A4', 500),
('D5', 250), ('C#5', 250), ('D5', 250),
('B4', 250), ('F5', 250), ('B4', 250),
('C5', 500), ('C5', 500), ('D5', 500),
('C5', 500), ('D5', 500)
]

for note, duration in melody:
    stop = instrument.play(note = note, instrument="Analog Saw.sf2")
    sleep(duration / 1000)
    stop()