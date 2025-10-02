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
        self.reset_button.pack_forget() # Hide reset button initially

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif")])
        if file_path:
            # Open and display the image
            image = Image.open(file_path)
            image.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo

            # Hide upload button and show reset button
            self.upload_button.pack_forget()
            self.reset_button.pack(pady=10)

    def reset(self):
        # Clear the image
        self.image_label.config(image='')
        self.image_label.image = None

        # Hide reset button and show upload button
        self.reset_button.pack_forget()
        self.upload_button.pack(pady=20)

if __name__ == "__main__":
    app = ImageUploader()
    app.mainloop()