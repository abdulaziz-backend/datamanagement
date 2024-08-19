import os
import tkinter as tk
from tkinter import ttk, messagebox
from concurrent.futures import ThreadPoolExecutor

class FileExplorerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom File Explorer")
        self.root.geometry("800x600")

        self.tree = ttk.Treeview(self.root)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.on_double_click)

        self.executor = ThreadPoolExecutor(max_workers=5)  # Create a thread pool

        # Populate tree with root directory
        self.populate_directory(os.path.expanduser("~"), "")

    def populate_directory(self, path, parent):
        # Clear existing tree items
        self.tree.delete(*self.tree.get_children(parent))

        # Use a thread pool to perform file system operations asynchronously
        future = self.executor.submit(self.get_directory_items, path)
        future.add_done_callback(lambda f: self.handle_directory_items(f.result(), parent))

    def get_directory_items(self, path):
        try:
            return sorted(os.listdir(path))
        except OSError:
            messagebox.showerror("Error", f"Unable to access directory: {path}")
            return []

    def handle_directory_items(self, items, parent):
        for item in items:
            item_path = os.path.join(parent, item)
            item_id = self.tree.insert(parent, "end", text=item, open=False)

            if os.path.isdir(item_path):
                self.tree.insert(item_id, "end")  # Dummy child to show expand icon

    def on_double_click(self, event):
        item_id = self.tree.selection()[0]
        item_path = self.get_item_path(item_id)

        if os.path.isfile(item_path):
            messagebox.showinfo("File Selected", f"You double-clicked on file: {item_path}")
        else:
            self.populate_directory(item_path, item_id)  # Expand directory

    def get_item_path(self, item_id):
        item_text = self.tree.item(item_id, "text")
        item_parent = self.tree.parent(item_id)

        if item_parent:
            parent_path = self.get_item_path(item_parent)
            return os.path.join(parent_path, item_text)
        else:
            return item_text  # Root directory

if __name__ == "__main__":
    root = tk.Tk()
    app = FileExplorerApp(root)
    root.mainloop()
