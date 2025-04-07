import os
import time
import threading
import tkinter as tk
from tkinter import ttk
from tagger import process_audio

WATCH_FOLDER = os.path.expanduser("~/Desktop/WatchAudio")
SUPPORTED_FORMATS = ('.mp3', '.wav', '.flac')

class ProfanityTaggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Local Profanity Tagger")
        self.root.geometry("700x400")

        # Treeview to display results
        self.tree = ttk.Treeview(root, columns=('File', 'Tag', 'Transcript'), show='headings')
        self.tree.heading('File', text='File Name')
        self.tree.heading('Tag', text='Profanity Tag')
        self.tree.heading('Transcript', text='Transcript')
        self.tree.column('File', width=150)
        self.tree.column('Tag', width=100)
        self.tree.column('Transcript', width=400)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Start background thread to watch the folder
        self.processed_files = set()
        self.running = True
        threading.Thread(target=self.watch_folder, daemon=True).start()

    def watch_folder(self):
        os.makedirs(WATCH_FOLDER, exist_ok=True)
        print(f"Watching: {WATCH_FOLDER}")

        while self.running:
            for fname in os.listdir(WATCH_FOLDER):
                if fname.endswith(SUPPORTED_FORMATS) and fname not in self.processed_files:
                    print(f"Found new file: {fname}")  # Debug print
                    path = os.path.join(WATCH_FOLDER, fname)
                    result = process_audio(path)
                    print(f"Processed: {result}")  # Debug print

                    # Insert the result into the treeview
                    self.tree.insert('', 'end', values=(os.path.basename(fname), result["tag"], result["transcript"]))
                    self.processed_files.add(fname)
            time.sleep(2)  # Poll every 2 seconds

    def stop(self):
        self.running = False
        print("Stopping...")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProfanityTaggerApp(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        app.stop()
