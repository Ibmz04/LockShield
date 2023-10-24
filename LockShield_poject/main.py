import os
import sys
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivy.resources import resource_add_path
from screen_manager_class import my_screen_manager

Window.fullscreen = 'auto'

class screen_manager(my_screen_manager):
    pass
class lockShieldMainClassApp(MDApp):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        reperexec = sys._MEIPASS
    else:
        reperexec = os.path.dirname(os.path.abspath(__file__))
    application_icone = os.path.join(reperexec, "Images/Application_logo.jpg")
    default_font = os.path.join(reperexec, "font/V5.ttf")

    manager = ObjectProperty(None)
    def build(self):
        self.title = "Lock Shield"
        self.icon = self.application_icone
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Dark"
        self.manager = screen_manager()
        return self.manager

    def hide_window(self):
        Window.minimize()

if __name__ == "__main__":
    lockShieldMainClassApp().run()

