import os
import subprocess
from control_panel_data import set_data
import threading
from time import sleep

def control_panel_thread():
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.togglebutton import ToggleButton
    from kivy.uix.button import Button
    from kivy.uix.scrollview import ScrollView
    from kivy.core.window import Window
    from kivy.config import Config
    import instrument_util

    global set_data

    # make sure it detects touch inputs only
    Config.set('kivy', 'desktop', 1)
    Config.set('input', 'mouse', 'mouse,disable_multitouch')

    class FullScreenApp(App):
        def build(self):
            # Set the window to fullscreen
            Window.fullscreen = 'auto'

            # Create a layout for the new window
            layout = BoxLayout(orientation='horizontal', spacing=10)

            # Create a vertical BoxLayout for the buttons
            button_layout = BoxLayout(
                orientation='vertical', size_hint=(None, 1), width=150)

            # Add ToggleButtons to the vertical layout
            for i in range(5):
                button = ToggleButton(
                    text=f'Octave {i+2}',
                    group='octaves',
                    allow_no_selection=False
                )
                button.bind(on_touch_down=self.on_octave_touch_down)

                # Set default state to enabled for Octave 4
                if i == 2:
                    button.state = 'down'

                button_layout.add_widget(button)

            # Add the vertical layout to the main horizontal layout
            layout.add_widget(button_layout)

            # Create a chord layout
            chord_layout = BoxLayout(
                orientation='vertical', size_hint=(None, None), width=300, height=200, spacing=10)
            chord_layout.pos_hint = {'center_y': 0.5}  # Center vertically

            chord_setting = BoxLayout(orientation='horizontal')
            no_chord_button = ToggleButton(
                text='None', group='major_minor', allow_no_selection=False)
            major_button = ToggleButton(
                text='Major', group='major_minor', allow_no_selection=False)
            minor_button = ToggleButton(
                text='Minor', group='major_minor', allow_no_selection=False)
            for button in [no_chord_button, major_button, minor_button]:
                button.bind(on_touch_down=self.on_chord_touch_down)
            no_chord_button.state = 'down'
            chord_setting.add_widget(no_chord_button)
            chord_setting.add_widget(major_button)
            chord_setting.add_widget(minor_button)

            inversions = BoxLayout(orientation='horizontal')
            no_inv_button = ToggleButton(
                text='Root', group='inversions', allow_no_selection=False)
            first_inv_button = ToggleButton(
                text='1st Inv', group='inversions', allow_no_selection=False)
            second_inv_button = ToggleButton(
                text='2nd Inv', group='inversions', allow_no_selection=False)
            for button in [no_inv_button, first_inv_button, second_inv_button]:
                button.bind(on_touch_down=self.on_inversion_touch_down)
            no_inv_button.state = 'down'
            inversions.add_widget(no_inv_button)
            inversions.add_widget(first_inv_button)
            inversions.add_widget(second_inv_button)

            chord_layout.add_widget(chord_setting)
            chord_layout.add_widget(inversions)

            # Add the chord layout to the main horizontal layout
            layout.add_widget(chord_layout)

            # Here lies the hold button. Rest in peace.

            # Create a scroll view for instruments
            self.scroll_layout = BoxLayout(
                orientation='vertical', size_hint_y=None, size_hint_x=None, width=150)
            self.scroll_layout.bind(minimum_height=self.scroll_layout.setter('height'))

            self.libraries = instrument_util.get_libraries()

            # Add toggle buttons to switch libraries
            self.library_buttons = BoxLayout(orientation='vertical', size_hint=(None, 1), width=150)
            for library in self.libraries:
                toggle_button = ToggleButton(
                    text=library['name'],
                    size_hint_y=None,
                    height=48,
                    group='libraries',
                    allow_no_selection=False
                )
                toggle_button.bind(on_touch_down=self.on_library_selected)

                # Set the first library to be selected by default
                if self.libraries.index(library) == 0:
                    toggle_button.state = 'down'

                self.library_buttons.add_widget(toggle_button)

            # Update instrument buttons for the default library (index 0)
            self.update_instrument_buttons(0)

            # Create a ScrollView and add the scroll layout to it
            scroll_view = ScrollView(size_hint=(
                None, 1), width=170, do_scroll_x=False, do_scroll_y=True)
            scroll_view.scroll_type = ['bars']
            scroll_view.bar_width = 20
            scroll_view.bar_color = [1, 1, 1, 1]
            scroll_view.bar_margin = 0
            scroll_view.scroll_y
            scroll_view.add_widget(self.scroll_layout)

            # Add the ScrollView to the main horizontal layout
            layout.add_widget(scroll_view)

            layout.add_widget(self.library_buttons)

            return layout

        def update_instrument_buttons(self, library_index):
            self.scroll_layout.clear_widgets()

            library = self.libraries[library_index]
            instruments = library['data']

            for i, data in enumerate(instruments):
                instrument_button = ToggleButton(
                    text=f"{i+1}. {data['name']}",
                    size_hint_y=None,
                    height=96,
                    group='instruments',
                    allow_no_selection=False,
                )
                instrument_button.bind(on_touch_down=self.on_instrument_touch_down)
                self.scroll_layout.add_widget(instrument_button)

                if i == 0:
                    instrument_button.state = 'down'

            #                 def on_library_selected(self, instance, touch):
            # selected_library_index = self.library_buttons.children.index(instance)
            # self.update_instrument_buttons(selected_library_index)
            # set_data('library', selected_library_index)

        def on_library_selected(self, instance, touch):
            if instance.collide_point(*touch.pos):
                library_index = self.libraries.index(
                    next((item for item in self.libraries if item['name'] == instance.text), None))
                set_data('instrument', 0)
                set_data('library', library_index)
                self.update_instrument_buttons(library_index)

        def on_octave_touch_down(self, instance, touch):
            if instance.collide_point(*touch.pos):
                print(f'Button {instance.text} pressed')
                octave = int(instance.text[-1])
                set_data('octave', octave)

        def on_chord_touch_down(self, instance, touch):
            if instance.collide_point(*touch.pos):
                print(f'Chord {instance.text} selected')
                set_data('chord', instance.text)

        def on_inversion_touch_down(self, instance, touch):
            conversion = {
                'Root': 0,
                '1st Inv': 1,
                '2nd Inv': 2
            }

            if instance.collide_point(*touch.pos):
                print(f'Inversion {instance.text} selected')
                set_data('inversion', conversion[instance.text])

        def on_instrument_touch_down(self, instance, touch):
            if instance.collide_point(*touch.pos):
                print(f'Instrument {instance.text} selected')
                # set the instrument index
                set_data('instrument', int(instance.text.split('.')[0]) - 1)


    if __name__ == '__main__':
        FullScreenApp().run()

# Create a new thread for running the control panel
control_panel_thread = threading.Thread(target=control_panel_thread)
control_panel_thread.start()

# Set up the control panel

# Main loop
from note_controller import loop as note_controller_loop
from note_controller import active_sensor_info
from led_controller import update_with_active_note_info
from instrument_util import *
import time

while True:
    sleep(1/50)

    note_controller_loop()
    update_with_active_note_info(active_sensor_info)

