import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import subprocess
import os

class SmartFileOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart File Organizer")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        self.path_var = tk.StringVar()
        self.conflict_mode = tk.StringVar(value="rename")

        tk.Label(root, text="📂 Smart File Organizer", font=("Segoe UI", 16, "bold")).pack(pady=10)

        frame_path = tk.Frame(root)
        frame_path.pack(pady=10, padx=10, fill="x")
        tk.Entry(frame_path, textvariable=self.path_var, width=60).pack(side="left", padx=5)
        tk.Button(frame_path, text="Select folder", command=self.browse_folder, bg="#0078D7", fg="white").pack(side="left")

        frame_mode = tk.Frame(root)
        frame_mode.pack(pady=5)
        tk.Label(frame_mode, text="Conflict mode:", font=("Segoe UI", 10)).pack(side="left", padx=5)
        ttk.Combobox(frame_mode, textvariable=self.conflict_mode, values=["rename", "skip"], width=10, state="readonly").pack(side="left")

        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=15)
        tk.Button(frame_buttons, text="Organize", command=self.run_organize, bg="#28A745", fg="white", width=15).grid(row=0, column=0, padx=5)
        tk.Button(frame_buttons, text="Dry Run", command=self.run_dry_run, bg="#FFC107", fg="black", width=15).grid(row=0, column=1, padx=5)
        tk.Button(frame_buttons, text="Undo", command=self.run_undo, bg="#DC3545", fg="white", width=15).grid(row=0, column=2, padx=5)

        tk.Label(root, text="Operations log:", font=("Segoe UI", 10, "bold")).pack(pady=(10, 0))
        self.output_text = scrolledtext.ScrolledText(root, width=80, height=15, font=("Consolas", 9))
        self.output_text.pack(padx=10, pady=5)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_var.set(folder)

    def run_command(self, args):
        if not self.path_var.get():
            messagebox.showwarning("Warning", "Select a folder first.")
            return

        command = ["python", "organizer.py", self.path_var.get()] + args
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        self.output_text.delete(1.0, tk.END)
        for line in process.stdout:
            self.output_text.insert(tk.END, line)
            self.output_text.see(tk.END)
            self.root.update_idletasks()

        process.wait()
        if process.returncode == 0:
            messagebox.showinfo("Success", "The operation was successfully completed.!")
        else:
            messagebox.showerror("Error", "There was a problem executing the script.")

    def run_organize(self):
        mode = ["--conflict-mode", self.conflict_mode.get()]
        self.run_command(mode)

    def run_dry_run(self):
        mode = ["--dry-run", "--conflict-mode", self.conflict_mode.get()]
        self.run_command(mode)

    def run_undo(self):
        self.run_command(["--undo"])


if __name__ == "__main__":
    root = tk.Tk()
    app = SmartFileOrganizerGUI(root)
    root.mainloop()



