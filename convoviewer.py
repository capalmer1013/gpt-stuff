import tkinter as tk
from tkinter import filedialog
import json

class ChatViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Viewer")
        self.root.geometry("500x500")

        self.text_box = tk.Text(self.root)
        self.text_box.pack(fill=tk.BOTH, expand=True)

        self.load_button = tk.Button(self.root, text="Load", command=self.load_file)
        self.load_button.pack()

    def load_file(self):
        file_path = filedialog.askopenfilename()
        with open(file_path, "r") as f:
            data = json.load(f)

        formatted_data = ""
        for message in data:
            formatted_data += f'{message["role"]}: {message["content"]}\n\n'

        self.text_box.delete("1.0", tk.END)
        self.text_box.insert(tk.END, formatted_data)

if __name__ == "__main__":
    root = tk.Tk()
    chat_viewer = ChatViewer(root)
    root.mainloop()
