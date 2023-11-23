from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.config import Config

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

        

        # Create a HOLD button
        hold_button = Button(
            text='Hold',
            size_hint=(None, None),
            size=(150, 150),
            pos_hint={'center_y': 0.5}
        )
        hold_button.bind(on_touch_down=self.on_hold_touch_down)

        # Add the HOLD button to the main layout
        layout.add_widget(hold_button)

        return layout

    def on_octave_touch_down(self, instance, touch):
        if instance.collide_point(*touch.pos):
            print(f'Button {instance.text} pressed')

    def on_hold_touch_down(self, instance, touch):
        if instance.collide_point(*touch.pos):
            print('HOLD button pressed')


if __name__ == '__main__':
    FullScreenApp().run()
