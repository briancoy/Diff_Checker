import tkinter as tk
from tkinter import scrolledtext
import difflib

# Function to compare the text and highlight the differences in the original text boxes
def compare_text():
    text1 = text_box1.get("1.0", tk.END)
    text2 = text_box2.get("1.0", tk.END)

    # Get the differences between the two texts
    diff = difflib.ndiff(text1.splitlines(), text2.splitlines())

    # Clear previous highlights
    text_box1.tag_remove("delete", "1.0", tk.END)
    text_box1.tag_remove("add", "1.0", tk.END)
    text_box2.tag_remove("delete", "1.0", tk.END)
    text_box2.tag_remove("add", "1.0", tk.END)

    # Variables to track line numbers in both text boxes
    line_num1 = 1
    line_num2 = 1

    # Apply color coding to the text in the original boxes
    for line in diff:
        if line.startswith("-"):  # Deletions (in red) in the first text box
            text_box1.tag_add("delete", f"{line_num1}.0", f"{line_num1}.end")
            line_num1 += 1
        elif line.startswith("+"):  # Additions (in yellow) in the second text box
            text_box2.tag_add("add", f"{line_num2}.0", f"{line_num2}.end")
            line_num2 += 1
        else:  # Context (no change)
            line_num1 += 1
            line_num2 += 1

# Create the main window
root = tk.Tk()
root.title("Text Comparator")
root.geometry("800x600")  # Initial size

# Create text boxes that resize with the window
text_box1 = scrolledtext.ScrolledText(root, wrap=tk.WORD)
text_box1.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10)

text_box2 = scrolledtext.ScrolledText(root, wrap=tk.WORD)
text_box2.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)

# Add text tags for different highlights
text_box1.tag_config("delete", foreground="red")
text_box2.tag_config("add", foreground="black", background="yellow")

# Create a button to compare the texts
compare_button = tk.Button(root, text="Compare Text", command=compare_text)
compare_button.pack(side=tk.BOTTOM, pady=10)

# Start the main event loop
root.mainloop()
