import tkinter as tk

def submit():
    print("Button clicked")

root = tk.Tk()

input_label = tk.Label(root, text="Input:")
input_label.pack()

input_entry = tk.Entry(root)
input_entry.pack()

submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack()

output_label = tk.Label(root, text="Output:")
output_label.pack()

output_textbox = tk.Text(root)
output_textbox.pack()

root.mainloop()