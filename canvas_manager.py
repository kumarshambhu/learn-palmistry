import tkinter as tk
from constants import big_text

LABEL_FONT = ("Helvetica", 10)

class CanvasManager:
    def __init__(self, main_app):
        self.main_app = main_app
        self.canvases_container = tk.Frame(self.main_app)
        self.canvas1()
        self.canvas2()
        self.canvas3()
        self.canvases_container.pack(pady=10, fill=tk.BOTH, expand=True)
        self.canvases_container.pack_forget()

    def on_configure(self, event):
        self.canvas3.configure(scrollregion=self.canvas3.bbox("all"))

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
