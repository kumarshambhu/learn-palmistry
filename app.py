import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageUploader(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Uploader")
        self.geometry("400x400")

        self.upload_button = tk.Button(self, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=20)

        self.image_label = tk.Label(self)
        self.image_label.pack(pady=10)

        self.reset_button = tk.Button(self, text="Reset", command=self.reset)
        self.reset_button.pack(pady=10)

        # Add a frame for zoom buttons
        self.zoom_frame = tk.Frame(self)
        self.zoom_in_button = tk.Button(self.zoom_frame, text="Zoom In", command=self.zoom_in)
        self.zoom_in_button.pack(side=tk.LEFT, padx=5)
        self.zoom_out_button = tk.Button(self.zoom_frame, text="Zoom Out", command=self.zoom_out)
        self.zoom_out_button.pack(side=tk.LEFT, padx=5)

        self.reset_button.pack_forget() # Hide reset button initially
        self.zoom_frame.pack_forget() # Hide zoom buttons initially

        self.original_image = None
        self.current_zoom = 1.0

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif")])
        if file_path:
            # Open and display the image
            self.original_image = Image.open(file_path)
            self.current_zoom = 1.0
            self.update_image_display()

            # Hide upload button and show reset and zoom buttons
            self.upload_button.pack_forget()
            self.reset_button.pack(pady=10)
            self.zoom_frame.pack(pady=5)

    def reset(self):
        # Clear the image
        self.image_label.config(image='')
        self.image_label.image = None
        self.original_image = None
        self.current_zoom = 1.0

        # Hide reset and zoom buttons and show upload button
        self.reset_button.pack_forget()
        self.zoom_frame.pack_forget()
        self.upload_button.pack(pady=20)

    def zoom_in(self):
        self.current_zoom *= 1.2
        self.update_image_display()

    def zoom_out(self):
        self.current_zoom /= 1.2
        self.update_image_display()

    def update_image_display(self):
        if self.original_image:
            width, height = self.original_image.size
            new_size = (int(width * self.current_zoom), int(height * self.current_zoom))

            # Use ANTIALIAS for resizing for better quality
            resized_image = self.original_image.resize(new_size, Image.Resampling.LANCZOS)

            photo = ImageTk.PhotoImage(resized_image)
            self.image_label.config(image=photo)
            self.image_label.image = photo

if __name__ == "__main__":
    app = ImageUploader()
    app.mainloop()