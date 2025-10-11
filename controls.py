import tkinter as tk
from styling_ui import image_style_button

class Controls:
    def __init__(self, main_app, event_handlers):
        self.main_app = main_app
        self.event_handlers = event_handlers
        self.controls_frame = tk.Frame(self.main_app)

        self.zoom_in_button = tk.Button(self.controls_frame, text="  Zoom In ", command=self.event_handlers.zoom_in)
        image_style_button(self.zoom_in_button, './images/zoom_in.png')
        self.zoom_in_button.pack(side=tk.LEFT, padx=5)

        self.zoom_out_button = tk.Button(self.controls_frame, text=" Zoom Out ", command=self.event_handlers.zoom_out)
        image_style_button(self.zoom_out_button, './images/zoom_out.png')
        self.zoom_out_button.pack(side=tk.LEFT, padx=5)

        self.grayscale_button = tk.Button(self.controls_frame, text="Grayscale", command=self.event_handlers.convert_to_grayscale,
                                          bg="#808080", relief="raised")
        self.grayscale_button.pack(side=tk.LEFT, padx=5)

        self.detect_hands_button = tk.Button(self.controls_frame, text=" Detect Hands ", command=self.event_handlers.detect_hands,
                                             relief="raised")
        image_style_button(self.detect_hands_button, './images/hand.jpg')
        self.detect_hands_button.pack(side=tk.LEFT, padx=5)

        self.remove_bg_button = tk.Button(self.controls_frame, text="Remove Background", command=self.event_handlers.remove_background)
        image_style_button(self.remove_bg_button, './images/eraser.png')
        self.remove_bg_button.pack(side=tk.LEFT, padx=5)

        self.controls_frame.pack(pady=5)
        self.controls_frame.pack_forget()
