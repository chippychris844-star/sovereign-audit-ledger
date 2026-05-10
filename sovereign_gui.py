import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import os

# --- CONFIGURATION ---
PYTHON_EXE = r"C:\Users\chipp\AppData\Roaming\Accio\pre-install\7d5a6d879db7\python\python.exe"
QUERY_SCRIPT = r"C:\Users\chipp\sovereign_query.py"

class SovereignApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sovereign Console // Resolution Assurance")
        # Fullscreen setup
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda e: self.root.attributes('-fullscreen', False))
        self.root.bind("<F11>", lambda e: self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen')))
        self.root.configure(bg="#000000")

        # Header
        self.header = tk.Label(
            root, text="RESOLUTION ASSURANCE // SOVEREIGN CONSOLE", 
            fg="#F1F5F9", bg="#000000", font=("JetBrains Mono", 24, "bold"), pady=40
        )
        self.header.pack()

        # Input Area
        self.input_box = tk.Entry(
            root, bg="#0A0A0A", fg="#00FF41", insertbackground="#00FF41",
            font=("JetBrains Mono", 16), borderwidth=1, relief="flat", highlightthickness=1, highlightbackground="#333333"
        )
        self.input_box.pack(fill="x", padx=100, pady=20)
        self.input_box.bind("<Return>", lambda e: self.run_query())
        self.input_box.focus_set()

        # Output Area
        self.output_area = scrolledtext.ScrolledText(
            root, bg="#000000", fg="#00FF41", font=("JetBrains Mono", 14),
            borderwidth=0, relief="flat", padx=40, pady=40, insertbackground="#00FF41"
        )
        self.output_area.pack(fill="both", expand=True, padx=100, pady=40)

        self.status = tk.Label(
            root, text="NODE: 01 | CORE: C: DRIVE | PERIMETER: SEALED | F11: FULLSCREEN | ESC: EXIT", 
            fg="#00FF41", bg="#000000", font=("JetBrains Mono", 10)
        )
        self.status.pack(side="bottom", pady=10)

    def run_query(self):
        query = self.input_box.get().strip()
        if not query:
            return

        self.output_area.delete(1.0, tk.END)
        self.output_area.insert(tk.END, "Processing through SQLite + Gemma...\n\n")
        self.root.update()

        try:
            # Execute the sovereign query script directly
            result = subprocess.check_output(
                [PYTHON_EXE, QUERY_SCRIPT, query], 
                stderr=subprocess.STDOUT, text=True
            )
            self.output_area.insert(tk.END, result)
        except subprocess.CalledProcessError as e:
            self.output_area.insert(tk.END, f"Error executing refinery: {e.output}")
        except Exception as e:
            self.output_area.insert(tk.END, f"Refinery Failure: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SovereignApp(root)
    root.mainloop()
