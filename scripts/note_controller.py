from sound import play
from instrument_util import *
from tof import get_sensor_binaries

BURST_INSTRUMENTS = [  # Instruments that we do not need to stop playing when we change notes
    "Acid SQ Neutral.sf2",
    "Piano.sf2"
]

# one table for each note in the octave (C-B)
active_sensor_info = {i: [] for i in range(1, 13)}

class NoteInstance:
    def __init__(self, instrument, note, hold=False):
        self.instrument = instrument
        self.note = note
        self.stop_func = None
        self.hold = hold

    def play(self):
        self.stop_func = play(self.instrument, self.note)

    def stop(self):
        if self.stop_func is not None:
            self.stop_func()
            self.stop_func = None

    def get_notes(self):
        return [self.note]

    def __eq__(self, other):
        return self.instrument == other.instrument and self.note == other.note
    
class ChordInstance:
    def __init__(self, instrument, notes, hold=False):
        self.instrument = instrument
        self.hold = hold
        self.notes = [NoteInstance(instrument, note, hold) for note in notes]

    def play(self):
        for note in self.notes:
            note.play()

    def stop(self):
        for note in self.notes:
            note.stop()

    def get_notes(self):
        return [instance.note for instance in self.notes]

    def __eq__(self, other):
        return self.instrument == other.instrument and self.notes == other.notes

def loop():
    binaries = get_sensor_binaries()
    holding = get_data('hold')

    for sensor_number, sensor_info in active_sensor_info.items():
        binary = binaries[sensor_number - 1]
        should_create_instance = binary == 1 and sensor_info is None
        clear_these = []

        # Check if we should create a new instance
        for instance in sensor_info:
            isBurst = instance.instrument in BURST_INSTRUMENTS

            if binary == 0: # If the sensor is not in range
                if isBurst or (not holding or (holding and not instance.hold)):
                    if not isBurst: instance.stop()
                    clear_these.append(instance)

        for instance in clear_these:
            sensor_info.remove(instance)

        for instance in sensor_info:
            if not instance.hold:
                should_create_instance = False

        if should_create_instance:

            print("Creating new instance for sensor", sensor_number)

            octave = get_selected_octave()
            chord = get_selected_chord()
            inversion = get_selected_inversion()
            instrument = get_selected_instrument()
            isBurst = instrument in BURST_INSTRUMENTS

            if chord != 'None':
                notes = create_chord(octave, chord, inversion)
                instance = ChordInstance(instrument, notes, holding if isBurst else False)
            else:
                note = sensor_to_note(sensor_number) + str(octave)
                instance = NoteInstance(instrument, note, holding if isBurst else False)

            instance.play()
            sensor_info.append(instance)

def stop_all():
    for sensor_info in active_sensor_info.values():
        for instance in sensor_info:
            instance.stop()
    active_sensor_info.clear()
    active_sensor_info.update({i: [] for i in range(1, 13)})

            