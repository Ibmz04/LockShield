import os
import threading
import decryption_setup
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.uix.popup import Popup
from kivy.utils import get_color_from_hex
from kivymd.uix.boxlayout import MDBoxLayout

Builder.load_file("decryption_main_file.kv")

decryption_key = str()
decryption_algorithm = "AES_CBC_128"
class Decryption_class(MDBoxLayout):
    decryption_label_text = ObjectProperty(None)
    decryption_progres_bar = ObjectProperty(None)
    decryption_file_mode = StringProperty("file")
    disabled_decryption_button = BooleanProperty(False)
    decryption_progress_bar_opacity = StringProperty("0")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def Decryption_data(self, dt):
        self.decryption_file_mode = str(dt.value)

    def show_decryption_setup(self):
        Popup(
            title = "Lock Shield",
            title_align = "center",
            title_color = get_color_from_hex("#1FA055"),
            title_size = 20,
            background_color = get_color_from_hex("#606060"),
            separator_color = get_color_from_hex("#1FA055"),
            size_hint = (.8, .4),
            auto_dismiss = False,
            content = Popup_decryption_content()
        ).open()

    def restart(self):
        global decryption_key, decryption_algorithm
        decryption_key = str()
        decryption_algorithm = "AES-CBC-128"
    def run_decryption(self, filechooser_path):
        success_decrypted = True
        def generate_key(length):
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=int(length),
                salt= b'salt_',
                iterations=100000
            )
            return kdf.derive(decryption_key.encode())

        def open_target_file(path_file):
            with open(path_file, 'rb') as encrypted_file:
                return encrypted_file.read(22)

        if self.decryption_file_mode == "file":
            str_path = filechooser_path.selection[0]
            if str_path[-7:] == ".shield":
                self.disabled_decryption_button = True
                self.decryption_label_text.text = "Decryption in progress...//"
                encryption_signature = open_target_file(str_path)
                try:
                    match encryption_signature:
                        case b"lockShield_AES_CBC_128":
                                decryption_setup.my_class_threading(str_path, generate_key(16)).AES_CBC_128()
                        case b"lockShield_AES_CBC_256":
                            decryption_setup.my_class_threading(str_path, generate_key(32)).AES_CBC_256()
                        case b"lockShield_AES_GCM_256":
                            decryption_setup.my_class_threading(str_path, generate_key(32)).AES_GCM_256()
                        case _:
                            self.decryption_label_text.text = "File not recognized"
                            success_decrypted = False
                except Exception as e:
                    if "Padding is incorrect." in f"{e}":
                        self.disabled_decryption_button = False
                        self.decryption_label_text.color = "red"
                        self.decryption_label_text.text = "Wrong decryption key, please try again!"
                else:
                    self.restart()
                    self.disabled_decryption_button = False
                    if success_decrypted: self.decryption_label_text.text = "Decryption completed"
            else:
                self.decryption_label_text.text = "File not recognized"
        else:
            for path, dirs, files in os.walk(str(filechooser_path.path)):
                for file in files:
                    str_path = os.path.join(path, file)
                    self.disabled_decryption_button, success_decrypted = True, True
                    if str_path[-7:] == ".shield":
                        self.decryption_progres_bar.value += 1
                        self.decryption_label_text.text = str(str_path)
                        try:
                            encryption_signature = open_target_file(str_path)
                            match encryption_signature:
                                case b"lockShield_AES_CBC_128":
                                    decryption_setup.my_class_threading(str_path, generate_key(16)).AES_CBC_128()
                                case b"lockShield_AES_CBC_256":
                                    decryption_setup.my_class_threading(str_path, generate_key(32)).AES_CBC_256()
                                case b"lockShield_AES_GCM_256":
                                    decryption_setup.my_class_threading(str_path, generate_key(32)).AES_GCM_256()
                                case _:
                                    self.decryption_label_text.text = "File not recognized"
                                    success_decrypted = False
                        except Exception as e:
                            if "Padding is incorrect." in "{}".format(e):
                                self.decryption_label_text.color = "red"
                                self.decryption_label_text.text = "Wrong decryption key, please try again!"
                                self.disabled_decryption_button = False
                        else:
                            self.disabled_decryption_button = False
                            self.decryption_label_text.color = "#1FA055"
                            if success_decrypted: self.decryption_label_text.text = "Decryption completed"
                    else:
                        self.decryption_label_text.text = "File not recognized"
            self.restart()
            self.disabled_decryption_button = False
            self.decryption_progres_bar.value = self.decryption_progres_bar.max

    def start_decryption(self, filechooser_path):
        def count():
            if self.decryption_file_mode == "folder":
                n = 0
                for path, dirs, files in os.walk(filechooser_path.path):
                    for file in files:
                        if file[-7:] == ".shield":
                            n += 1
                self.decryption_progres_bar.max = n
                self.decryption_progress_bar_opacity = "1"
            else:
                self.decryption_progress_bar_opacity = "0"
            self.decryption_progres_bar.value = 0
            self.decryption_label_text.color = "#1FA055"

        def open_popup(popup_text):
            Popup(
                title="Lock Shield",
                title_align="center",
                title_color="red",
                title_size=15,
                background_color=get_color_from_hex("#606060"),
                separator_color=get_color_from_hex("#606060"),
                size_hint=(.5, .2),
                content=Alert_Popup_decryption_content(str(popup_text))
            ).open()

        if not  decryption_key or decryption_key == "" or \
                (self.decryption_file_mode == "file" and filechooser_path.selection == []):
            open_popup("Error, you must specify the decryption key or the target file before \nlaunching the decryption")
        else:
            count()
            my_thread = threading.Thread(target=self.run_decryption, args=[filechooser_path])
            my_thread.start()


class Alert_Popup_decryption_content(MDBoxLayout):
    popup_text = StringProperty(None)
    def __init__(self,  message, **kwargs):
        super().__init__(**kwargs)
        self.popup_text = str(message)


class Popup_decryption_content(MDBoxLayout):
    show_decryption_password = BooleanProperty(True)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def show_decryption_key(self, dt):
        if dt.active:
            self.show_decryption_password = False
        else:
            self.show_decryption_password = True

    def restart_decryption_setup(self):
        global decryption_key
        decryption_key = None

    def save_decryption_setup(self, dt):
        global decryption_key
        decryption_key = str(dt.text)