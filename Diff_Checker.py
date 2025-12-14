import tkinter as tk
from tkinter import scrolledtext
import difflib

# Function to compare the text and display the differences
def compare_text():
    text1 = text_box1.get("1.0", tk.END)
    text2 = text_box2.get("1.0", tk.END)

    # Get the differences between the two texts
    diff = difflib.ndiff(text1.splitlines(), text2.splitlines())
    differences = '\n'.join(diff)

    # Show the differences in a new window
    diff_window = tk.Toplevel(root)
    diff_window.title("Differences")
    
    diff_text = scrolledtext.ScrolledText(diff_window, wrap=tk.WORD, width=80, height=20)
    diff_text.pack(fill=tk.BOTH, expand=True)
    diff_text.insert(tk.INSERT, differences)

# Create the main window
root = tk.Tk()
root.title("Text Comparator")

# Create two text boxes
text_box1 = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=15)
text_box1.grid(row=0, column=0, padx=10, pady=10)

text_box2 = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=15)
text_box2.grid(row=0, column=1, padx=10, pady=10)

# Create a button to compare the texts
compare_button = tk.Button(root, text="Compare Text", command=compare_text)
compare_button.grid(row=1, column=0, columnspan=2, pady=10)

# Start the main event loop
root.mainloop()
