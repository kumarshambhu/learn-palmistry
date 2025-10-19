import tkinter as tk
from constants import big_text

LABEL_FONT = ("Helvetica", 10)
# Update scroll region when the frame changes\\\\
class CanvasManager:
    def __init__(self, main_app):
        self.main_app = main_app
        self.canvases_container = tk.Frame(self.main_app)
        self.canvas2()
        self.canvas3()
        self.canvases_container.pack(fill=tk.BOTH, expand=True)
        self.canvases_container.pack_forget()

    def canvas2(self):
        # Canvas 2 for the image
        self.canvas_frame2 = tk.Frame(self.canvases_container)
        self.canvas2 = tk.Canvas(self.canvas_frame2)
        self.v_scrollbar2 = tk.Scrollbar(self.canvas_frame2, orient=tk.VERTICAL, command=self.canvas2.yview)
        self.h_scrollbar2 = tk.Scrollbar(self.canvas_frame2, orient=tk.HORIZONTAL, command=self.canvas2.xview)
        self.canvas2.configure(yscrollcommand=self.v_scrollbar2.set, xscrollcommand=self.h_scrollbar2.set)
        self.v_scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scrollbar2.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas_image2 = None
        self.canvas_frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

    def canvas3(self):
        # Create canvas and scrollbar
        canvas = tk.Canvas(self.canvases_container, borderwidth=0)
        scrollbar = tk.Scrollbar(self.canvases_container, orient="vertical", command=canvas.yview)
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
        self.label3 = tk.Text(frame,  wrap="word", )
        #self.label3.pack(fill="both", expand=True)
        self.label3.pack(padx=10, pady=10)
        self.label3.insert("1.0", big_sentence)

        # Update scroll region
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame.bind("<Configure>", on_frame_configure)
