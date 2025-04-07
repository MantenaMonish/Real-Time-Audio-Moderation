# ui_windows.py
import os
import time
import threading
import tkinter as tk
from tkinter import ttk
from tagger import process_audio

# Use a universal location on Windows (e.g., Documents\WatchAudio)
WATCH_FOLDER = r"C:\profanity_tagger\WatchAudio"
SUPPORTED_FORMATS = ('.mp3', '.wav', '.flac')

class ProfanityTaggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Profanity Tagger - Windows")
        self.root.geometry("750x450")

        # Treeview GUI table
        self.tree = ttk.Treeview(root, columns=('File', 'Tag', 'Transcript'), show='headings')
        self.tree.heading('File', text='File Name')
        self.tree.heading('Tag', text='Profanity Tag')
        self.tree.heading('Transcript', text='Transcript')
        self.tree.column('File', width=180)
        self.tree.column('Tag', width=100)
        self.tree.column('Transcript', width=440)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.processed_files = set()
        self.running = True
        threading.Thread(target=self.watch_folder, daemon=True).start()

    def watch_folder(self):
        os.makedirs(WATCH_FOLDER, exist_ok=True)
        print(f"Watching folder: {WATCH_FOLDER}")
        while self.running:
            for fname in os.listdir(WATCH_FOLDER):
                if fname.endswith(SUPPORTED_FORMATS) and fname not in self.processed_files:
                    path = os.path.join(WATCH_FOLDER, fname)
                    result = process_audio(path)
                    self.tree.insert('', 'end', values=(
                        os.path.basename(fname), result["tag"], result["transcript"]
                    ))
                    self.processed_files.add(fname)
            time.sleep(2)

    def stop(self):
        self.running = False

if __name__ == "__main__":
    root = tk.Tk()
    app = ProfanityTaggerApp(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        app.stop()
