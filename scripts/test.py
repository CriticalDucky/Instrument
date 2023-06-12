import instrument
from time import sleep

melody = [
('C4', 500), # Twin-
('C4', 500), # kle
('G4', 500), # twin-
('G4', 500), # kle
('A4', 500), # lit-
('A4', 500), # tle
('G4', 1000), # star
('F4', 500), # How
('F4', 500), # I
('E4', 500), # won-
('E4', 500), # der
('D4', 500), # what
('D4', 500), # you
('C4', 1000), # are
('G4', 500), # Up
('G4', 500), # a-
('F4', 500), # bove
('F4', 500), # the
('E4', 500), # world
('E4', 500), # so
('D4', 1000), # high
('G4', 500), # Like
('G4', 500), # a
('F4', 500), # dia-
('F4', 500), # mond
('E4', 500), # in
('E4', 500), # the
('D4', 1000), # sky
('C4', 500), # Twin-
('C4', 500), # kle
('G4', 500), # twin-
('G4', 500), # kle
('A4', 500), # lit-
('A4', 500), # tle
('G4', 1000) # star
]

for note, duration in melody:
    stop = instrument.play(note = note)
    sleep(duration / 1000)
    stop()