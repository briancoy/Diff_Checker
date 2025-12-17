import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import difflib

# --- Logic Functions ---

def load_file(text_widget):
    """Opens a file dialog and loads the selected file into the given text widget."""
    filepath = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            text_widget.delete("1.0", tk.END)
            text_widget.insert("1.0", content)
    except Exception as e:
        messagebox.showerror("Error", f"Could not open file: {e}")

def compare_text():
    """Compares text, highlights differences, and ignores difflib metadata."""
    text1 = text_box1.get("1.0", tk.END).splitlines()
    text2 = text_box2.get("1.0", tk.END).splitlines()

    # Clear previous highlights
    text_box1.tag_remove("delete", "1.0", tk.END)
    text_box2.tag_remove("add", "1.0", tk.END)

    diff = difflib.ndiff(text1, text2)

    line_num1 = 1
    line_num2 = 1

    for line in diff:
        code = line[:2]
        
        if code.startswith('?'):
            continue

        if code.startswith('-'):
            text_box1.tag_add("delete", f"{line_num1}.0", f"{line_num1}.end")
            line_num1 += 1
        elif code.startswith('+'):
            text_box2.tag_add("add", f"{line_num2}.0", f"{line_num2}.end")
            line_num2 += 1
        else:
            line_num1 += 1
            line_num2 += 1

# --- Scroll Synchronization Logic ---
is_scrolling = False  # Flag to prevent infinite scroll loops

def sync_scroll(producer, consumer, first, last):
    """
    Handles scrolling for 'producer' and updates 'consumer' if sync is enabled.
    """
    global is_scrolling
    
    # Update the producer's internal scrollbar (standard behavior)
    producer.vbar.set(first, last)

    # If Sync is On and we aren't already processing a scroll event
    if sync_var.get() and not is_scrolling:
        is_scrolling = True
        try:
            # Move the consumer to the exact same position
            consumer.yview_moveto(first)
        finally:
            is_scrolling = False

# --- GUI Setup ---
root = tk.Tk()
root.title("Text Comparator with Sync Scroll")
root.geometry("1000x700")

# 1. Top Button Frame
button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X, pady=5)

# Load Buttons
btn_load1 = tk.Button(button_frame, text="Load Left File", command=lambda: load_file(text_box1))
btn_load1.pack(side=tk.LEFT, padx=10)

btn_load2 = tk.Button(button_frame, text="Load Right File", command=lambda: load_file(text_box2))
btn_load2.pack(side=tk.RIGHT, padx=10)

# Sync Checkbox (Centered)
sync_var = tk.BooleanVar(value=False) # Default to False (Off)
chk_sync = tk.Checkbutton(button_frame, text="Sync Scrolling", variable=sync_var, font=("Arial", 10, "bold"))
chk_sync.pack(side=tk.TOP)

# 2. Main Text Area
text_frame = tk.Frame(root)
text_frame.pack(expand=True, fill=tk.BOTH, padx=10)

text_box1 = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, width=40)
text_box1.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=(0, 5))

text_box2 = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, width=40)
text_box2.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=(5, 0))

# 3. Configure Scroll Callbacks
# We override the default scroll command to trigger our sync function
text_box1.config(yscrollcommand=lambda f, l: sync_scroll(text_box1, text_box2, f, l))
text_box2.config(yscrollcommand=lambda f, l: sync_scroll(text_box2, text_box1, f, l))

# Tags for highlighting
text_box1.tag_config("delete", foreground="red", background="#ffe6e6")
text_box2.tag_config("add", foreground="black", background="yellow")

# 4. Compare Button
compare_button = tk.Button(root, text="Compare Text", command=compare_text, font=("Arial", 12, "bold"))
compare_button.pack(side=tk.BOTTOM, pady=15)

root.mainloop()