from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.config import Config

# make sure it detects touch inputs only
Config.set('kivy', 'desktop', 1)
Config.set('input', 'mouse', 'mouse,disable_multitouch')

class ScrollableButton(Button):
    def on_touch_down(self, touch):
        if super(ScrollableButton, self).on_touch_down(touch):
            return True  # Event has been handled by the button
        return False  # Event has not been handled, allowing it to propagate

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

        # Create a HOLD button
        hold_button = Button(
            text='Hold',
            size_hint=(None, None),
            size=(150, 150),
            pos_hint={'center_y': 0.5}
        )
        hold_button.bind(
            on_touch_down=self.on_hold_touch_down,
            on_touch_up=self.on_hold_touch_up
        )

        # Add the HOLD button to the main layout
        layout.add_widget(hold_button)

        # Create a chord layout
        chord_layout = BoxLayout(
            orientation='vertical', size_hint=(None, None), width=300, height=200, spacing=10)
        chord_layout.pos_hint = {'center_y': 0.5}  # Center vertically

        major_minor = BoxLayout(orientation='horizontal')
        major_button = ToggleButton(text='Major', group='major_minor', allow_no_selection=False)
        minor_button = ToggleButton(text='Minor', group='major_minor', allow_no_selection=False)

        major_button.state = 'down'

        major_minor.add_widget(major_button)
        major_minor.add_widget(minor_button)

        inversions = BoxLayout(orientation='horizontal')
        no_inv_button = ToggleButton(text='No Inv', group='inversions', allow_no_selection=False)
        first_inv_button = ToggleButton(text='1st Inv', group='inversions', allow_no_selection=False)
        second_inv_button = ToggleButton(text='2nd Inv', group='inversions', allow_no_selection=False)

        no_inv_button.state = 'down'

        inversions.add_widget(no_inv_button)
        inversions.add_widget(first_inv_button)
        inversions.add_widget(second_inv_button)

        chord_layout.add_widget(major_minor)
        chord_layout.add_widget(inversions)

        # Add the chord layout to the main horizontal layout
        layout.add_widget(chord_layout)

        # Create a scroll view for instruments
        scroll_layout = BoxLayout(orientation='vertical', size_hint_y=None, width=150)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))

        # Add 10 instruments to the scroll layout
        for i in range(10):
            instrument_button = ScrollableButton(
                text=f'Instrument {i + 1}',
                size_hint_y=None,
                height=96
            )
            scroll_layout.add_widget(instrument_button)

        # Create a ScrollView and add the scroll layout to it
        scroll_view = ScrollView(size_hint=(None, 1), width=150, do_scroll_x=False, do_scroll_y=True)
        scroll_view.add_widget(scroll_layout)

        # Add the ScrollView to the main horizontal layout
        layout.add_widget(scroll_view)

        return layout

    def on_octave_touch_down(self, instance, touch):
        if instance.collide_point(*touch.pos):
            print(f'Button {instance.text} pressed')

    def on_hold_touch_down(self, instance, touch):
        if instance.collide_point(*touch.pos):
            print('HOLD button pressed')

    def on_hold_touch_up(self, instance, touch):
        if instance.collide_point(*touch.pos):
            print('HOLD button released')

    def on_instrument_touch_down(self, instance, touch):
        if instance.collide_point(*touch.pos):
            print(f'Instrument {instance.text} selected')


if __name__ == '__main__':
    FullScreenApp().run()
