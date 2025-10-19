import tkinter as tk

root = tk.Tk()
root.title("Multiline Styled Text with Tags")

text = tk.Text(root, height=5)
text.pack()

# Insert text
text.insert("1.0", "This is a bold word, and this is italic.\n")
text.insert("2.0", "This line has red and green words.\n")

# Define styles
text.tag_add("bold", "1.10", "1.14")
text.tag_config("bold", font=("Arial", 12, "bold"))

text.tag_add("italic", "1.34", "1.40")
text.tag_config("italic", font=("Times", 12, "italic"))

text.tag_add("red", "2.14", "2.17")
text.tag_config("red", foreground="red")

text.tag_add("green", "2.22", "2.27")
text.tag_config("green", foreground="green")

# Make it read-only
text.config(state="disabled")

root.mainloop()
