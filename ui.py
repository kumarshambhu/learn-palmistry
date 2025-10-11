import tkinter as tk
from tkinter import filedialog, PhotoImage

from PIL import Image, ImageTk

from constants import big_text
from image_processor import ImageProcessor
from styling_ui import zoom_in_style_button, zoom_out_style_button, image_style_button


BG_COLOR = "#F5F5F5"
TEXT_COLOR = "#333333"
BTN_FONT = ("Helvetica", 10, "bold")
LABEL_FONT = ("Helvetica", 10)


# Function to update scroll region


class ImageUploader(tk.Tk):
    def on_configure(self, event):
        self.canvas3.configure(scrollregion=self.canvas3.bbox("all"))
    def __init__(self):
        super().__init__()
        self.title("Image Uploader")
        self.geometry("1200x400")

        self.image_processor = ImageProcessor()
        self._init_ui()
        self._init_state()

    def canvas1(self):
        # Canvas 1 for original image
        self.canvas_frame1 = tk.Frame(self.canvases_container)
        self.canvas1 = tk.Canvas(self.canvas_frame1)
        self.v_scrollbar1 = tk.Scrollbar(self.canvas_frame1, orient=tk.VERTICAL, command=self.canvas1.yview)
        self.h_scrollbar1 = tk.Scrollbar(self.canvas_frame1, orient=tk.HORIZONTAL, command=self.canvas1.xview)
        self.canvas1.configure(yscrollcommand=self.v_scrollbar1.set, xscrollcommand=self.h_scrollbar1.set)
        self.v_scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scrollbar1.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas_image1 = None
        self.canvas_frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

    def canvas2(self):
        # Canvas 2 for processed image
        self.canvas_frame2 = tk.Frame(self.canvases_container)
        self.canvas2 = tk.Canvas(self.canvas_frame2)
        self.v_scrollbar2 = tk.Scrollbar(self.canvas_frame2, orient=tk.VERTICAL, command=self.canvas2.yview)
        self.h_scrollbar2 = tk.Scrollbar(self.canvas_frame2, orient=tk.HORIZONTAL, command=self.canvas2.xview)
        self.canvas2.configure(yscrollcommand=self.v_scrollbar2.set, xscrollcommand=self.h_scrollbar2.set)
        self.v_scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scrollbar2.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas_image2 = None
        self.canvas_frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))

    def canvas3(self):
        self.canvas_frame3 = tk.Frame(self.canvases_container)
        self.canvas_frame3.pack(fill="both", expand=True)

        self.canvas3 = tk.Canvas(self.canvas_frame3)
        self.canvas3.pack(side="left", fill="both", expand=True)

        # Add a vertical scrollbar linked to the canvas
        scrollbar = tk.Scrollbar(self.canvas_frame3, orient="vertical", command=self.canvas3.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas3.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas to hold the content
        self.content_frame = tk.Frame(self.canvas3, bg="white")
        self.canvas3.create_window((0, 0), window=self.content_frame, anchor="nw")

        self.v_scrollbar3 = tk.Scrollbar(self.canvas_frame3, orient=tk.VERTICAL, command=self.canvas3.yview)
        self.h_scrollbar3 = tk.Scrollbar(self.canvas_frame3, orient=tk.HORIZONTAL, command=self.canvas3.xview)
        self.canvas3.configure(yscrollcommand=self.v_scrollbar3.set, xscrollcommand=self.h_scrollbar3.set)
        self.v_scrollbar3.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scrollbar3.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.content_frame.bind("<Configure>", self.on_configure)
        self.result_label = tk.Label(self.content_frame, text=f"{big_text}",
                                     bg="white", anchor="w", justify="left",
                                     wraplength=380,
                                     font=LABEL_FONT)
        self.result_label.pack(
            anchor="nw", padx=10, pady=5)

    def _init_ui(self):
        self.upload_button = tk.Button(self, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=20)

        self.canvases_container = tk.Frame(self)
        self.canvas1()
        self.canvas2()
        self.canvas3()

        self.reset_button = tk.Button(self, text="Reset", command=self.reset, fg="white", bg="#FF0000")
        self.reset_button.pack(pady=10)

        self.controls_frame = tk.Frame(self)
        self.zoom_in_button = tk.Button(self.controls_frame, text="  Zoom In ", command=self.zoom_in)
        image_style_button(self.zoom_in_button, './images/zoom_in.png')
        self.zoom_in_button.pack(side=tk.LEFT, padx=5)

        self.zoom_out_button = tk.Button(self.controls_frame, text=" Zoom Out ", command=self.zoom_out)
        image_style_button(self.zoom_out_button, './images/zoom_out.png')
        self.zoom_out_button.pack(side=tk.LEFT, padx=5)

        self.grayscale_button = tk.Button(self.controls_frame, text="Grayscale", command=self.convert_to_grayscale,
                                          bg="#808080", relief="raised")
        self.grayscale_button.pack(side=tk.LEFT, padx=5)

        self.detect_hands_button = tk.Button(self.controls_frame, text=" Detect Hands ", command=self.detect_hands,
                                             relief="raised")
        image_style_button(self.detect_hands_button, './images/hand.jpg')
        self.detect_hands_button.pack(side=tk.LEFT, padx=5)

        self.remove_bg_button = tk.Button(self.controls_frame, text="Remove Background", command=self.remove_background)
        image_style_button(self.remove_bg_button, './images/eraser.png')
        self.remove_bg_button.pack(side=tk.LEFT, padx=5)

        self.reset_button.pack_forget()
        self.controls_frame.pack_forget()
        self.canvases_container.pack_forget()

    def _init_state(self):
        self.original_image = None
        self.processed_image = None
        self.is_grayscale = False
        self.current_zoom = 1.0
        self.photo1 = None
        self.photo2 = None
        self.hand_landmarks = None

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif")])
        if file_path:
            self.original_image = Image.open(file_path)
            self.processed_image = self.original_image.copy()
            self._reset_state()
            self.update_image_display()
            self._show_controls()

    def _reset_state(self):
        if self.original_image:
            self.processed_image = self.original_image.copy()
        self.is_grayscale = False
        self.current_zoom = 1.0
        self.hand_landmarks = None

    def _show_controls(self):
        self.upload_button.pack_forget()
        self.canvases_container.pack(pady=10, fill=tk.BOTH, expand=True)
        self.reset_button.pack(pady=10)
        self.controls_frame.pack(pady=5)

    def reset(self):
        if self.canvas_image1:
            self.canvas1.delete(self.canvas_image1)
            self.canvas_image1 = None
        if self.canvas_image2:
            self.canvas2.delete(self.canvas_image2)
            self.canvas_image2 = None
        self._init_state()
        self._hide_controls()

    def _hide_controls(self):
        self.canvases_container.pack_forget()
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
        self.result_label.config(text=big_text)
        if self.original_image:
            self.processed_image = self.image_processor.remove_background(self.original_image)
            self.update_image_display()

    def zoom_in(self):
        self.current_zoom *= 1.2
        self.update_image_display()

    def zoom_out(self):
        self.current_zoom /= 1.2
        self.update_image_display()

    def update_image_display(self):
        if self.original_image:
            # Update original image canvas
            width1, height1 = self.original_image.size
            new_size1 = (int(width1 * self.current_zoom), int(height1 * self.current_zoom))
            resized_image1 = self.original_image.resize(new_size1, Image.Resampling.LANCZOS)
            self.photo1 = ImageTk.PhotoImage(resized_image1)
            if self.canvas_image1:
                self.canvas1.delete(self.canvas_image1)
            self.canvas_image1 = self.canvas1.create_image(0, 0, anchor=tk.NW, image=self.photo1)
            self.canvas1.config(scrollregion=self.canvas1.bbox(tk.ALL))

            # Update processed image canvas
            image_to_display = self.processed_image.copy()
            if self.is_grayscale:
                image_to_display = self.image_processor.convert_to_grayscale(image_to_display)
            if self.hand_landmarks:
                image_to_display = self.image_processor.draw_hand_landmarks(image_to_display, self.hand_landmarks)

            width2, height2 = image_to_display.size
            new_size2 = (int(width2 * self.current_zoom), int(height2 * self.current_zoom))
            resized_image2 = image_to_display.resize(new_size2, Image.Resampling.LANCZOS)

            self.photo2 = ImageTk.PhotoImage(resized_image2)
            if self.canvas_image2:
                self.canvas2.delete(self.canvas_image2)
            self.canvas_image2 = self.canvas2.create_image(0, 0, anchor=tk.NW, image=self.photo2)
            self.canvas2.config(scrollregion=self.canvas2.bbox(tk.ALL))
