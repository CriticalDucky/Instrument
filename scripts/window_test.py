from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window

class FullScreenApp(App):
    def build(self):
        # Set the window to fullscreen
        Window.fullscreen = 'auto'

        # Create a layout for the new window
        layout = BoxLayout(orientation='horizontal')

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
            button.bind(on_touch_down=self.on_touch_down)

            # Set default state to enabled for Octave 4
            if i == 2:
                button.state = 'down'

            button_layout.add_widget(button)

        # Add the vertical layout to the main horizontal layout
        layout.add_widget(button_layout)

        return layout

    def on_touch_down(self, instance, touch):
        if instance.collide_point(*touch.pos):
            print(f'Button {instance.text} pressed')


if __name__ == '__main__':
    FullScreenApp().run()
