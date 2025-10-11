import tkinter as tk

from constants import big_text

# Create the main window
root = tk.Tk()
root.title("Scrollable Canvas with Text")

# Create a frame to hold the canvas and scrollbar
container = tk.Frame(root)
container.pack(fill="both", expand=True)

# Create a canvas inside the frame
canvas = tk.Canvas(container, width=400, height=300, bg="white")
canvas.pack(side="left", fill="both", expand=True)

# Add a vertical scrollbar linked to the canvas
scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas to hold the content
content_frame = tk.Frame(canvas, bg="white")
canvas.create_window((0, 0), window=content_frame, anchor="nw")

# Function to update scroll region
def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

content_frame.bind("<Configure>", on_configure)

# Add lots of text labels to demonstrate scrolling
long_text = (
    "This is a long block of text that demonstrates how to use a canvas with a scrollbar. "
    "Each line is a separate label widget inside a frame embedded in the canvas. "
    "You can scroll through the content using the scrollbar on the right."
)

tk.Label(content_frame, text=f"{big_text}", bg="white", anchor="w", justify="left", wraplength=380).pack(anchor="w", padx=10, pady=5)

# Run the application
root.mainloop()
