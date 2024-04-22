from sound import play
from notation import *
from tof import get_sensor_binaries
import colorsys

# one table for each note in the octave (C-B)
active_sensor_info = {i: [] for i in range(1, 13)}

class NoteInstance:
    def __init__(self, library, instrument, note):
        self.library = library
        self.instrument = instrument
        self.note = note
        self.stop_func = None
        self.led_primed = False

    def play(self):
        self.stop_func = play(self.library, self.instrument, self.note)

    def stop(self):
        if self.stop_func is not None:
            self.stop_func()
            self.stop_func = None

    def get_notes(self):
        return [self.note]
    
    # This function is used by LEDS for animation.
    def set_led_primed(self):
        self.led_primed = True
    
class ChordInstance:
    def __init__(self, library, instrument, notes, original_note=None):
        self.library = library
        self.instrument = instrument
        self.notes = [NoteInstance(instrument, note) for note in notes]
        self.led_primed = False
        self.original_note = original_note

    def play(self):
        for note in self.notes:
            note.play()

    def stop(self):
        for note in self.notes:
            note.stop()

    def get_notes(self):
        return [instance.note for instance in self.notes]
    
    def set_led_primed(self):
        self.led_primed = True

def loop():
    binaries = get_sensor_binaries()
    # print(binaries)

    for sensor_number, sensor_info in active_sensor_info.items():
        binary = binaries[sensor_number - 1]
        should_create_instance = binary == 1
        clear_these = []

        # Check if we should create a new instance, and set led_primed to True
        for instance in sensor_info:
            isBurst = is_instrument_burst(instance.instrument)

            if isBurst and not instance.led_primed:
                instance.set_led_primed()

            if binary == 0: # If the sensor is not in range
                if not isBurst: instance.stop()
                clear_these.append(instance)

        for instance in clear_these:
            sensor_info.remove(instance)

        for instance in sensor_info:
            should_create_instance = False

        if should_create_instance:
            octave = get_selected_octave()
            chord_type = get_selected_chord()
            inversion = get_selected_inversion()
            library = get_selected_library()
            instrument = get_selected_instrument()

            note = sensor_to_note(sensor_number) + str(octave)

            if chord_type != 'None':
                notes = create_chord(note, chord_type, inversion)
                instance = ChordInstance(library, instrument, notes, note)
            else:
                instance = NoteInstance(library, instrument, note)

            instance.play()
            sensor_info.append(instance)

def stop_all():
    for sensor_info in active_sensor_info.values():
        for instance in sensor_info:
            instance.stop()
    active_sensor_info.clear()
    active_sensor_info.update({i: [] for i in range(1, 13)})

            