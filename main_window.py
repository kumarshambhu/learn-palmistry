import tkinter as tk

import app_utils
from image_processor import ImageProcessor
from state_manager import StateManager
from canvas_manager import CanvasManager
from controls import Controls
from event_handlers import EventHandlers

class ImageUploader(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Uploader")
        self.geometry("800x400")

        self.image_processor = ImageProcessor()
        self.state_manager = StateManager()
        self.canvas_manager = CanvasManager(self)
        self.event_handlers = EventHandlers(self, self.state_manager, self.canvas_manager, None)
        self.controls = Controls(self, self.event_handlers)
        self.event_handlers.controls = self.controls

        self._init_ui()

    def _init_ui(self):
        self.upload_button = tk.Button(self, text="Upload Image", command=self.event_handlers.upload_image)
        self.upload_button.pack()

        # self.reset_button = tk.Button(self, text="Reset", command=self.event_handlers.reset, fg="white", bg="#FF0000")
        # self.reset_button.pack(pady=10)

        # self.hand_type_label = tk.Label(self, text="", font=("Arial", 14, "bold"))
        # self.hand_type_label.pack(pady=5)

        #self.reset_button.pack_forget()

    # def update_hand_type_label(self, text):
    #     self.hand_type_label.config(text=text)
    def update_hand_details_data(self, key):
        data = app_utils.read_file("details.json", key)
        self.canvas_manager.label3.delete("1.0", "end")
        if 'basic' in data:
            self.canvas_manager.label3.insert("1.0", data["basic"] + "\n")
            self.canvas_manager.label3.tag_add("bold", "1.0", "1.end")
            self.canvas_manager.label3.tag_config("bold", font=("Arial", 12, "bold"))
        if 'personality' in data:
            self.canvas_manager.label3.insert("2.0", data["personality"] + "\n")
            self.canvas_manager.label3.tag_add("bold_red", "2.0", "2.end")
            self.canvas_manager.label3.tag_config("bold_red", foreground="blue", font=("Arial", 12))

