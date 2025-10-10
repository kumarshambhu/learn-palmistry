import tkinter as tk
from PIL import Image, ImageTk


def zoom_in_style_button(button):
    button.config(
        bg="blue",
        fg="white",
        font=("Helvetica", 12, "bold"),
        activebackground="#45a049",
        activeforeground="white",
        relief="flat",
        cursor="hand2"
    )


def zoom_out_style_button(button):
    button.config(
        bg="blue",
        fg="white",
        font=("Helvetica", 12, "bold"),
        activebackground="#45a049",
        activeforeground="white",
        relief="flat",
        cursor="hand2"
    )


def image_style_button(button, image_location):
    img = Image.open(image_location)
    img = img.resize((20, 20))  # Resize as needed
    photo = ImageTk.PhotoImage(img)

    # Keep a reference to the image to prevent garbage collection
    button.image = photo
    button.config(
        font=("Helvetica", 8),
        relief="raised",
        cursor="hand2",
        image=photo,
        borderwidth=5,
        compound="left"
    )
