import tkinter as tk

root = tk.Tk()
root.title("Dynamic Text Styling")

text = tk.Text(root)
text.pack()

# Insert styled text
text.insert("1.0", "Air Hand (Intellectual and Communicative)\n")
text.insert("2.0", "Air hands suggest an intellectual, communicative, and analytical personality. These individuals are curious, sociable, and always full of ideas. They thrive on mental stimulation, enjoy discussing abstract concepts, and are natural communicators. They can sometimes be restless and prone to overthinking.\n")

# Define tag with style
text.tag_add("bold", "1.0", "1.end")
text.tag_config("bold", font=("Arial", 12, "bold"))

text.tag_add("bold_red", "2.0", "2.end")
text.tag_config("bold_red", foreground="red", font=("Arial", 12, "bold"))

root.mainloop()
