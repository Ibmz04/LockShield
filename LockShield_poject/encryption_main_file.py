import os
import random
import threading
import win32clipboard
import encryption_setup

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.uix.popup import Popup
from kivy.utils import get_color_from_hex
from kivymd.uix.boxlayout import MDBoxLayout
Builder.load_file("encryption_main_file.kv")


encryption_key = str()
encryption_algorithm = "AES-CBC-128"
class Encryption_class(MDBoxLayout):
    encryption_label_text = ObjectProperty(None)
    encryption_progres_bar = ObjectProperty(None)
    progress_bar_opacity = StringProperty("0")
    encryption_file_mode = StringProperty("file")
    disabled_encryption_button = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def encryption_data(self, dt):
        self.encryption_file_mode = str(dt.value)

    def show_encryption_setup(self):
        Popup(
            title = "Lock Shield",
            title_align = "center",
            title_color = get_color_from_hex("#1FA055"),
            title_size = 20,
            background_color = get_color_from_hex("#606060"),
            separator_color = get_color_from_hex("#1FA055"),
            size_hint = (.9, .9),
            auto_dismiss = False,
            content = Popup_encryption_content()
        ).open()

    def restart(self):
        global encryption_key, encryption_algorithm
        encryption_key = str()
        encryption_algorithm = "AES-CBC-128"

    def run_encryption(self, filechooser_path):
        def generate_key(length):
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=int(length),
                salt=b'salt_',
                iterations=100000
            )
            return kdf.derive(encryption_key.encode())

        if self.encryption_file_mode == "file":
            self.disabled_encryption_button = True
            str_path = filechooser_path.selection[0]
            if str_path[-7:] != ".shield":
                self.encryption_label_text.text = "Encryption in progress...//"
                try:
                    match encryption_algorithm:
                        case "AES-CBC-128":
                            encryption_setup.my_class_threading(str_path, generate_key(16)).AES_CBC_128()
                        case "AES-CBC-256":
                            encryption_setup.my_class_threading(str_path, generate_key(32)).AES_CBC_256()
                        case "AES-GCM-256":
                            encryption_setup.my_class_threading(str_path, generate_key(32)).AES_GCM_256()
                        case _:
                            pass
                except Exception as e:
                    print(e)
                    self.encryption_label_text.color = "red"
                    self.encryption_label_text.text = "Eroor during encryption, try again!"
                else:
                    self.encryption_label_text.color = "#1FA055"
                    self.encryption_label_text.text = "Encryption completed"
            else:
                self.encryption_label_text.text = "This file is already encrypted"
        else:
            for path, dirs, files in os.walk(str(filechooser_path.path)):
                for file in files:
                    str_path = os.path.join(path, file)
                    self.disabled_encryption_button = True
                    if str_path[-7:] != ".shield":
                        try:
                            self.encryption_progres_bar.value += 1
                            self.encryption_label_text.text = str(str_path)
                            match encryption_algorithm:
                                case "AES-CBC-128":
                                   encryption_setup.my_class_threading(str_path, generate_key(16)).AES_CBC_128()
                                case "AES-CBC-256":
                                    encryption_setup.my_class_threading(str_path, generate_key(32)).AES_CBC_256()
                                case "AES-GCM-256":
                                    encryption_setup.my_class_threading(str_path, generate_key(32)).AES_GCM_256()
                                case _:
                                    pass
                        except:
                            self.encryption_label_text.color = "red"
                            self.encryption_label_text.text = "Eroor during encryption, try again!"
                        else:
                            self.encryption_label_text.color = "#1FA055"
                            self.encryption_label_text.text = "Encryption completed"
        self.restart()
        self.disabled_encryption_button = False
        self.encryption_progres_bar.value = self.encryption_progres_bar.max


    def start_encryption(self, filechooser_path):
        def count():
            if self.encryption_file_mode == "folder":
                n = 0
                for path, dirs, files in os.walk(filechooser_path.path):
                    for file in files:
                        if  file[-7:] != ".shield":
                            n += 1
                self.encryption_progres_bar.max = n
                self.progress_bar_opacity = "1"
            else:
                self.progress_bar_opacity = "0"
            self.encryption_progres_bar.value = 0
            self.encryption_label_text.color = "#1FA055"

        if not encryption_key or encryption_key == "" or \
                (self.encryption_file_mode == "file" and filechooser_path.selection == []):
            Popup(
                title="Lock Shield",
                title_align="center",
                title_color="red",
                title_size=15,
                background_color=get_color_from_hex("#606060"),
                separator_color=get_color_from_hex("#606060"),
                size_hint=(.5, .2),
                content=Alert_Popup_encryption_content()
            ).open()
        else:
            count()
            my_thread = threading.Thread(target=self.run_encryption, args=[filechooser_path])
            my_thread.start()



class Alert_Popup_encryption_content(MDBoxLayout):
    pass
class Popup_encryption_content(MDBoxLayout):
    generated_key_text = StringProperty("")
    generated_key_color = StringProperty("white")
    show_encryption_password = BooleanProperty(True)
    write_encryption_key_state = BooleanProperty(True)
    generate_encryption_key_state = BooleanProperty(True)
    copy_disabled_button = BooleanProperty(True)
    copy_opacity_button = StringProperty("0")
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.generated_key = str()

    def choose_encryption_algorithm(self, dt):
        global encryption_algorithm
        encryption_algorithm = str(dt.value)

    def show_encryption_key(self, dt):
        if dt.active:
            self.show_encryption_password = False
        else:
            self.show_encryption_password = True

    def show_encryption_key_mode(self, dt):
        if dt.state == "down":
            if dt.value == "WriteKey":
                self.write_encryption_key_state = False
                self.generate_encryption_key_state = True
                self.generated_key_text = ""
                self.copy_disabled_button, self.copy_opacity_button = False, "0"
            elif dt.value == "GenerateKey":
                self.generate_encryption_key_state = False
                self.write_encryption_key_state = True
        else:
            self.write_encryption_key_state = True
            self.generate_encryption_key_state = True

    def generate_key(self, lenght):
        self.generated_key = str()
        try:
            input_text = int(lenght.text)
            if input_text > 256:
                self.generated_key_text = "The lenght of the key is too long"
                self.generated_key_color = "red"
            elif input_text < 8:
                self.generated_key_text = "You cannot generate a key less than 8 character"
                self.generated_key_color = "red"
            else:
                self.generated_key_color = "#1FA055"
                value = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
                for i in range(0, input_text):
                    val = random.choice(value)
                    self.generated_key += val
                self.generated_key_text = str(self.generated_key)
                self.copy_disabled_button, self.copy_opacity_button = False, "1"
        except:
            self.generated_key_text = "The lenght of the key must be a numeric number"
            self.generated_key_color = "red"


    def copy_encryption_key(self):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(self.generated_key)
        win32clipboard.CloseClipboard()

    def save_encryption_setup(self, dt):
        global encryption_key
        if not self.write_encryption_key_state:
            encryption_key = str(dt.text)
        elif not self.generate_encryption_key_state:
            encryption_key = str(self.generated_key)


    def restart_encryption_setup(self):
        global encryption_key
        encryption_key = str()