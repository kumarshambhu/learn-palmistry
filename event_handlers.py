from tkinter import filedialog
from PIL import Image, ImageTk
from constants import big_text
import tkinter as tk

class EventHandlers:
    def __init__(self, main_app, state_manager, canvas_manager, controls):
        self.main_app = main_app
        self.state_manager = state_manager
        self.canvas_manager = canvas_manager
        self.controls = controls

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif")])
        if file_path:
            self.state_manager.original_image = Image.open(file_path)
            self.state_manager.processed_image = self.state_manager.original_image.copy()
            self.state_manager._reset_state()
            self.update_image_display()
            self._show_controls()

    def _show_controls(self):
        self.main_app.upload_button.pack_forget()
        self.canvas_manager.canvases_container.pack(pady=10, fill=tk.BOTH, expand=True)
        self.main_app.reset_button.pack(pady=10)
        self.controls.controls_frame.pack(pady=5)

    def reset(self):
        if self.canvas_manager.canvas_image1:
            self.canvas_manager.canvas1.delete(self.canvas_manager.canvas_image1)
            self.canvas_manager.canvas_image1 = None
        if hasattr(self.main_app, 'hand_type_label'):
            self.main_app.hand_type_label.config(text="")
        self.state_manager.__init__()
        self._hide_controls()

    def _hide_controls(self):
        self.canvas_manager.canvases_container.pack_forget()
        self.main_app.reset_button.pack_forget()
        self.controls.controls_frame.pack_forget()
        self.main_app.upload_button.pack(pady=20)

    def convert_to_grayscale(self):
        self.state_manager.is_grayscale = not self.state_manager.is_grayscale
        self.update_image_display()

    def detect_hands(self):
        if self.state_manager.original_image:
            self.state_manager.hand_landmarks = self.main_app.image_processor.detect_hands(self.state_manager.original_image)
            self.update_image_display()

    def remove_background(self):
        self.canvas_manager.result_label.config(text=big_text)
        if self.state_manager.original_image:
            self.state_manager.processed_image = self.main_app.image_processor.remove_background(self.state_manager.original_image)
            self.update_image_display()

    def zoom_in(self):
        self.state_manager.current_zoom *= 1.2
        self.update_image_display()

    def zoom_out(self):
        self.state_manager.current_zoom /= 1.2
        self.update_image_display()

    def detect_hand_type(self):
        if self.state_manager.original_image:
            if not self.state_manager.hand_landmarks:
                self.detect_hands()  # Ensure landmarks are detected first

            if self.state_manager.hand_landmarks:
                hand_type = self.main_app.image_processor.detect_hand_type(self.state_manager.hand_landmarks)
                self.main_app.update_hand_type_label(hand_type)
            else:
                self.main_app.update_hand_type_label("No hands detected to classify.")

    def update_image_display(self):
        if self.state_manager.original_image:
            image_to_display = self.state_manager.original_image.copy()

            if self.state_manager.is_grayscale:
                image_to_display = self.main_app.image_processor.convert_to_grayscale(image_to_display)
            if self.state_manager.hand_landmarks:
                image_to_display = self.main_app.image_processor.draw_hand_landmarks(image_to_display, self.state_manager.hand_landmarks)

            # Update the single canvas
            width, height = image_to_display.size
            new_size = (int(width * self.state_manager.current_zoom), int(height * self.state_manager.current_zoom))
            resized_image = image_to_display.resize(new_size, Image.Resampling.LANCZOS)

            self.state_manager.photo1 = ImageTk.PhotoImage(resized_image)
            if self.canvas_manager.canvas_image1:
                self.canvas_manager.canvas1.delete(self.canvas_manager.canvas_image1)

            self.canvas_manager.canvas_image1 = self.canvas_manager.canvas1.create_image(0, 0, anchor=tk.NW, image=self.state_manager.photo1)
            self.canvas_manager.canvas1.config(scrollregion=self.canvas_manager.canvas1.bbox(tk.ALL))
