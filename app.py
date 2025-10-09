import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import mediapipe as mp
import numpy as np

class ImageUploader(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Uploader")
        self.geometry("600x600")

        self.upload_button = tk.Button(self, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=20)

        # Create a frame for the canvas and scrollbars
        self.canvas_frame = tk.Frame(self)
        self.canvas = tk.Canvas(self.canvas_frame)
        self.v_scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.h_scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)

        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas_image = None

        self.reset_button = tk.Button(self, text="Reset", command=self.reset)
        self.reset_button.pack(pady=10)

        # Add a frame for control buttons
        self.controls_frame = tk.Frame(self)
        self.zoom_in_button = tk.Button(self.controls_frame, text="Zoom In", command=self.zoom_in)
        self.zoom_in_button.pack(side=tk.LEFT, padx=5)
        self.zoom_out_button = tk.Button(self.controls_frame, text="Zoom Out", command=self.zoom_out)
        self.zoom_out_button.pack(side=tk.LEFT, padx=5)
        self.grayscale_button = tk.Button(self.controls_frame, text="Grayscale", command=self.convert_to_grayscale)
        self.grayscale_button.pack(side=tk.LEFT, padx=5)
        self.detect_hands_button = tk.Button(self.controls_frame, text="Detect Hands", command=self.detect_hands)
        self.detect_hands_button.pack(side=tk.LEFT, padx=5)

        self.remove_bg_button = tk.Button(self.controls_frame, text="Remove Background", command=self.remove_background)
        self.remove_bg_button.pack(side=tk.LEFT, padx=5)

        self.reset_button.pack_forget() # Hide reset button initially
        self.controls_frame.pack_forget() # Hide controls frame initially
        self.canvas_frame.pack_forget() # Hide canvas frame initially

        self.original_image = None
        self.is_grayscale = False
        self.current_zoom = 1.0
        self.photo = None # To prevent garbage collection
        self.hand_landmarks = None

        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils

        # Initialize MediaPipe Selfie Segmentation
        self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
        self.selfie_segmentation = self.mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif")])
        if file_path:
            # Open and display the image
            self.original_image = Image.open(file_path)
            self.is_grayscale = False
            self.current_zoom = 1.0
            self.update_image_display()

            # Hide upload button and show canvas, reset, and control buttons
            self.upload_button.pack_forget()
            self.canvas_frame.pack(pady=10, fill=tk.BOTH, expand=True)
            self.reset_button.pack(pady=10)
            self.controls_frame.pack(pady=5)

    def reset(self):
        # Clear the image from canvas
        if self.canvas_image:
            self.canvas.delete(self.canvas_image)
            self.canvas_image = None
        self.original_image = None
        self.is_grayscale = False
        self.current_zoom = 1.0
        self.hand_landmarks = None

        # Hide canvas, reset, and control buttons and show upload button
        self.canvas_frame.pack_forget()
        self.reset_button.pack_forget()
        self.controls_frame.pack_forget()
        self.upload_button.pack(pady=20)

    def convert_to_grayscale(self):
        self.is_grayscale = not self.is_grayscale
        self.update_image_display()

    def detect_hands(self):
        if self.original_image:
            # Convert PIL image to OpenCV format
            open_cv_image = cv2.cvtColor(np.array(self.original_image), cv2.COLOR_RGB2BGR)

            # Process the image and find hands
            results = self.hands.process(cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB))

            self.hand_landmarks = results.multi_hand_landmarks
            self.update_image_display()

    def remove_background(self):
        if self.original_image:
            # Convert PIL image to OpenCV format
            image_np = cv2.cvtColor(np.array(self.original_image), cv2.COLOR_RGB2BGR)

            # Process the image for selfie segmentation
            results = self.selfie_segmentation.process(image_np)

            # Create a mask from the segmentation results
            mask = results.segmentation_mask > 0.9  # Threshold for segmentation
            mask = mask.astype(np.uint8)

            # Create a white background
            white_background = np.ones_like(image_np) * 255

            # Apply the mask to the original image
            # The mask needs to be 3-channels to be applied to a 3-channel image
            mask_3_channel = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            no_bg_image = np.where(mask_3_channel == 1, image_np, white_background)

            # Convert the result back to a PIL image
            self.original_image = Image.fromarray(cv2.cvtColor(no_bg_image, cv2.COLOR_BGR2RGB))

            # Update the image display
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
                image_to_display = image_to_display.convert('L')

            if self.hand_landmarks:
                # Convert PIL image to OpenCV format for drawing
                image_np = np.array(image_to_display)
                if image_np.ndim == 2:  # Grayscale image
                    annotated_image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2BGR)
                else:  # Color image
                    annotated_image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

                for hand_landmarks in self.hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        annotated_image_np,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS)

                # Convert back to PIL Image
                image_to_display = Image.fromarray(cv2.cvtColor(annotated_image_np, cv2.COLOR_BGR2RGB))

            width, height = image_to_display.size
            new_size = (int(width * self.current_zoom), int(height * self.current_zoom))
            resized_image = image_to_display.resize(new_size, Image.Resampling.LANCZOS)

            self.photo = ImageTk.PhotoImage(resized_image)  # Keep a reference
            if self.canvas_image:
                self.canvas.delete(self.canvas_image)

            self.canvas_image = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

if __name__ == "__main__":
    app = ImageUploader()
    app.mainloop()