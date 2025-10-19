import tkinter as tk

root = tk.Tk()
root.title("Scrollable Label with Big Sentence")
root.geometry("500x300")

# Create canvas and scrollbar
canvas = tk.Canvas(root, borderwidth=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# Create a frame inside the canvas
frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

# Big sentence (long paragraph)
big_sentence = (
    "You can keep adding more text here to simulate a large block of content that needs to be scrolled "
    "vertically. This is useful for displaying logs, long descriptions, or any text-heavy UI element."
)

# Add the label
label = tk.Label(frame, text=big_sentence, wraplength=480, justify="left", anchor="nw")
label.pack(fill="both", expand=True)

# Update scroll region
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame.bind("<Configure>", on_frame_configure)

root.mainloop()
