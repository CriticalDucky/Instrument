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
        # Add widgets or customize the layout as needed

        # Add ToggleButtons to the layout
        for i in range(5):
            button = ToggleButton(text=f'Octave {i+2}', size_hint=(1, None), height=100, group='octaves')
            button.bind(on_touch_down=self.on_touch_down)
            layout.add_widget(button)

        return layout

    def on_touch_down(self, instance, touch):
        print(f'Button {instance.text} pressed')

if __name__ == '__main__':
    FullScreenApp().run()
