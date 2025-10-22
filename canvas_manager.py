import tkinter as tk
from constants import big_text

LABEL_FONT = ("Helvetica", 10)
# Update scroll region when the frame changes
class CanvasManager:
    def __init__(self, main_app):
        self.label3 = None
        self.main_app = main_app
        self.canvases_container = tk.Frame(self.main_app)
        self.canvas_frame2 = None
        self.canvas2 = None
        self.v_scrollbar2 = None
        self.h_scrollbar2 = None
        self.canvas_image2 = None
        self._create_canvas2()
        self._create_canvas3()
        self.canvases_container.pack(expand=True)
        self.canvases_container.pack_forget()

    def _create_canvas2(self):
        # Canvas 2 for the image
        self.canvas_frame2 = tk.Frame(self.canvases_container)
        self.canvas2 = tk.Canvas(self.canvas_frame2)
        self.v_scrollbar2 = tk.Scrollbar(self.canvas_frame2, orient="vertical", command=self.canvas2.yview)
        self.h_scrollbar2 = tk.Scrollbar(self.canvas_frame2, orient="horizontal", command=self.canvas2.xview)
        self.canvas2.configure(yscrollcommand=self.v_scrollbar2.set, xscrollcommand=self.h_scrollbar2.set)
        self.v_scrollbar2.pack(side="right", fill="y")
        self.h_scrollbar2.pack(side="bottom", fill="x")
        self.canvas2.pack(side="left", fill="both", expand=True)
        self.canvas_image2 = None
        self.canvas_frame2.pack(side="left", fill="both", expand=True, padx=(0, 5))

    def _create_canvas3(self):
        # Create canvas and scrollbar
        canvas = tk.Canvas(self.canvases_container, borderwidth=0)
        scrollbar = tk.Scrollbar(self.canvases_container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Create a frame inside the canvas
        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        # Add the label
        self.label3 = tk.Text(frame,  wrap="word", )
        self.label3.pack(padx=10, pady=10)
        self.label3.insert("1.0", big_text)

        # Update scroll region
        def on_frame_configure(_):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame.bind("<Configure>", on_frame_configure)
