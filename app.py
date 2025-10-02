import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

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

        # Add a frame for zoom buttons
        self.zoom_frame = tk.Frame(self)
        self.zoom_in_button = tk.Button(self.zoom_frame, text="Zoom In", command=self.zoom_in)
        self.zoom_in_button.pack(side=tk.LEFT, padx=5)
        self.zoom_out_button = tk.Button(self.zoom_frame, text="Zoom Out", command=self.zoom_out)
        self.zoom_out_button.pack(side=tk.LEFT, padx=5)

        self.reset_button.pack_forget() # Hide reset button initially
        self.zoom_frame.pack_forget() # Hide zoom buttons initially
        self.canvas_frame.pack_forget() # Hide canvas frame initially

        self.original_image = None
        self.current_zoom = 1.0
        self.photo = None # To prevent garbage collection

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif")])
        if file_path:
            # Open and display the image
            self.original_image = Image.open(file_path)
            self.current_zoom = 1.0
            self.update_image_display()

            # Hide upload button and show canvas, reset, and zoom buttons
            self.upload_button.pack_forget()
            self.canvas_frame.pack(pady=10, fill=tk.BOTH, expand=True)
            self.reset_button.pack(pady=10)
            self.zoom_frame.pack(pady=5)

    def reset(self):
        # Clear the image from canvas
        if self.canvas_image:
            self.canvas.delete(self.canvas_image)
            self.canvas_image = None
        self.original_image = None
        self.current_zoom = 1.0

        # Hide canvas, reset, and zoom buttons and show upload button
        self.canvas_frame.pack_forget()
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

            resized_image = self.original_image.resize(new_size, Image.Resampling.LANCZOS)

            self.photo = ImageTk.PhotoImage(resized_image) # Keep a reference
            if self.canvas_image:
                self.canvas.delete(self.canvas_image)

            self.canvas_image = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

if __name__ == "__main__":
    app = ImageUploader()
    app.mainloop()