import tkinter as tk
from tkinter import filedialog, PhotoImage

from PIL import Image, ImageTk

from image_processor import ImageProcessor
from styling_ui import zoom_in_style_button, zoom_out_style_button, image_style_button


class ImageUploader(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Uploader")
        self.geometry("600x600")

        self.image_processor = ImageProcessor()
        self._init_ui()
        self._init_state()

    def _init_ui(self):

        zoom_in_img = PhotoImage(file="images/zoom_in.png")



        self.upload_button = tk.Button(self, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=20)

        self.canvas_frame = tk.Frame(self)
        self.canvas = tk.Canvas(self.canvas_frame)
        self.v_scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.h_scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)

        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas_image = None

        self.reset_button = tk.Button(self, text="Reset", command=self.reset, fg="white", bg="#FF0000")
        self.reset_button.pack(pady=10)

        self.controls_frame = tk.Frame(self)
        self.zoom_in_button = tk.Button(self.controls_frame, text="  Zoom In ", command=self.zoom_in)
        image_style_button(self.zoom_in_button, './images/zoom_in.png')
        self.zoom_in_button.pack(side=tk.LEFT, padx=5)

        self.zoom_out_button = tk.Button(self.controls_frame, text=" Zoom Out ", command=self.zoom_out)
        image_style_button(self.zoom_out_button, './images/zoom_out.png')
        self.zoom_out_button.pack(side=tk.LEFT, padx=5)

        self.grayscale_button = tk.Button(self.controls_frame, text="Grayscale", command=self.convert_to_grayscale,  bg="#808080", relief="raised")
        self.grayscale_button.pack(side=tk.LEFT, padx=5)

        self.detect_hands_button = tk.Button(self.controls_frame, text=" Detect Hands ", command=self.detect_hands, relief="raised")
        image_style_button(self.detect_hands_button, './images/hand.jpg')
        self.detect_hands_button.pack(side=tk.LEFT, padx=5)

        self.remove_bg_button = tk.Button(self.controls_frame, text="Remove Background", command=self.remove_background)
        image_style_button(self.remove_bg_button, './images/eraser.png')
        self.remove_bg_button.pack(side=tk.LEFT, padx=5)

        self.reset_button.pack_forget()
        self.controls_frame.pack_forget()
        self.canvas_frame.pack_forget()

    def _init_state(self):
        self.original_image = None
        self.is_grayscale = False
        self.current_zoom = 1.0
        self.photo = None
        self.hand_landmarks = None

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif")])
        if file_path:
            self.original_image = Image.open(file_path)
            self._reset_state()
            self.update_image_display()
            self._show_controls()

    def _reset_state(self):
        self.is_grayscale = False
        self.current_zoom = 1.0
        self.hand_landmarks = None

    def _show_controls(self):
        self.upload_button.pack_forget()
        self.canvas_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        self.reset_button.pack(pady=10)
        self.controls_frame.pack(pady=5)

    def reset(self):
        if self.canvas_image:
            self.canvas.delete(self.canvas_image)
            self.canvas_image = None
        self._init_state()
        self._hide_controls()

    def _hide_controls(self):
        self.canvas_frame.pack_forget()
        self.reset_button.pack_forget()
        self.controls_frame.pack_forget()
        self.upload_button.pack(pady=20)

    def convert_to_grayscale(self):
        self.is_grayscale = not self.is_grayscale
        self.update_image_display()

    def detect_hands(self):
        if self.original_image:
            self.hand_landmarks = self.image_processor.detect_hands(self.original_image)
            self.update_image_display()

    def remove_background(self):
        if self.original_image:
            self.original_image = self.image_processor.remove_background(self.original_image)
            self.update_image_display()

    def zoom_in(self):
        self.current_zoom *= 1.2
        self.update_image_display()

    def zoom_out(self):
        self.current_zoom /= 1.2
        self.update_image_display()

    def update_image_display(self):
        if self.original_image:
            image_to_display = self.original_image.copy()

            if self.is_grayscale:
                image_to_display = self.image_processor.convert_to_grayscale(image_to_display)

            if self.hand_landmarks:
                image_to_display = self.image_processor.draw_hand_landmarks(image_to_display, self.hand_landmarks)

            width, height = image_to_display.size
            new_size = (int(width * self.current_zoom), int(height * self.current_zoom))
            resized_image = image_to_display.resize(new_size, Image.Resampling.LANCZOS)

            self.photo = ImageTk.PhotoImage(resized_image)
            if self.canvas_image:
                self.canvas.delete(self.canvas_image)

            self.canvas_image = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))