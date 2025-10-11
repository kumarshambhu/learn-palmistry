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
        if self.canvas_manager.canvas_image2:
            self.canvas_manager.canvas2.delete(self.canvas_manager.canvas_image2)
            self.canvas_manager.canvas_image2 = None
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
            self.state_manager.hand_landmarks, self.state_manager.handedness = self.main_app.image_processor.detect_hands(self.state_manager.original_image)
            if self.state_manager.hand_landmarks:
                self.state_manager.gestures = [self.main_app.image_processor.get_hand_gesture(landmarks) for landmarks in self.state_manager.hand_landmarks]
            self.update_image_display()
            self.canvas_manager.update_hand_info_label()

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

    def update_image_display(self):
        if self.state_manager.original_image:
            # Update original image canvas
            width1, height1 = self.state_manager.original_image.size
            new_size1 = (int(width1 * self.state_manager.current_zoom), int(height1 * self.state_manager.current_zoom))
            resized_image1 = self.state_manager.original_image.resize(new_size1, Image.Resampling.LANCZOS)
            self.state_manager.photo1 = ImageTk.PhotoImage(resized_image1)
            if self.canvas_manager.canvas_image1:
                self.canvas_manager.canvas1.delete(self.canvas_manager.canvas_image1)
            self.canvas_manager.canvas_image1 = self.canvas_manager.canvas1.create_image(0, 0, anchor=tk.NW, image=self.state_manager.photo1)
            self.canvas_manager.canvas1.config(scrollregion=self.canvas_manager.canvas1.bbox(tk.ALL))

            # Update processed image canvas
            image_to_display = self.state_manager.processed_image.copy()
            if self.state_manager.is_grayscale:
                image_to_display = self.main_app.image_processor.convert_to_grayscale(image_to_display)
            if self.state_manager.hand_landmarks:
                image_to_display = self.main_app.image_processor.draw_hand_landmarks(image_to_display, self.state_manager.hand_landmarks, self.state_manager.handedness, self.state_manager.gestures)

            width2, height2 = image_to_display.size
            new_size2 = (int(width2 * self.state_manager.current_zoom), int(height2 * self.state_manager.current_zoom))
            resized_image2 = image_to_display.resize(new_size2, Image.Resampling.LANCZOS)

            self.state_manager.photo2 = ImageTk.PhotoImage(resized_image2)
            if self.canvas_manager.canvas_image2:
                self.canvas_manager.canvas2.delete(self.canvas_manager.canvas_image2)
            self.canvas_manager.canvas_image2 = self.canvas_manager.canvas2.create_image(0, 0, anchor=tk.NW, image=self.state_manager.photo2)
            self.canvas_manager.canvas2.config(scrollregion=self.canvas_manager.canvas2.bbox(tk.ALL))
