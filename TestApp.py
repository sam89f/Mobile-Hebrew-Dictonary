 #Hebrew Dictionary mobile aplication python file
#==============================================================================

#This file displays the UI, and the main fuction buttons and input text field, while the .kv file
#displays the the keyboard input keys for the letters of the Hebrew alphabet along with other
#manipulation fuctions.

#qpy:kivy
#qpy:fullscreen
from kivy.app import App
from kivy.uix.button import Button
class TestApp(App):
    def build(self):
        return Button(text='Hello World')    
TestApp().run()