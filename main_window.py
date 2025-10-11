import tkinter as tk
from image_processor import ImageProcessor
from state_manager import StateManager
from canvas_manager import CanvasManager
from controls import Controls
from event_handlers import EventHandlers

class ImageUploader(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Uploader")
        self.geometry("1200x400")

        self.image_processor = ImageProcessor()
        self.state_manager = StateManager()
        self.canvas_manager = CanvasManager(self)
        self.event_handlers = EventHandlers(self, self.state_manager, self.canvas_manager, None)
        self.controls = Controls(self, self.event_handlers)
        self.event_handlers.controls = self.controls

        self._init_ui()

    def _init_ui(self):
        self.upload_button = tk.Button(self, text="Upload Image", command=self.event_handlers.upload_image)
        self.upload_button.pack(pady=20)

        self.reset_button = tk.Button(self, text="Reset", command=self.event_handlers.reset, fg="white", bg="#FF0000")
        self.reset_button.pack(pady=10)

        self.reset_button.pack_forget()
