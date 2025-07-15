from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib
import os

# --- Core Logic Functions ---

def get_file_hash(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for block in iter(lambda: f.read(4096), b""):
                sha256.update(block)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None

def load_hash(file_path):
    try:
        with open(file_path + ".hash", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_hash(file_path, hash_value):
    with open(file_path + ".hash", "w") as f:
        f.write(hash_value)

def delete_saved_hash():
    path = file_path.get()
    if os.path.exists(path + ".hash"):
        os.remove(path + ".hash")
        result_text.set("🗑️ Saved hash deleted.")
    else:
        result_text.set("ℹ️ No saved hash to delete.")

# --- GUI Handlers ---

def select_file():
    path = filedialog.askopenfilename()
    if path:
        file_path.set(path)
        result_text.set("📂 File selected. Click 'Verify' to check integrity.")

def verify_file():
    path = file_path.get()
    if not path or not os.path.exists(path):
        messagebox.showerror("Error", "Please select a valid file.")
        return

    current_hash = get_file_hash(path)
    saved_hash = load_hash(path)

    if saved_hash:
        if current_hash == saved_hash:
            result = "✅ File is intact. No changes detected."
        else:
            result = "⚠️ WARNING: File has been modified!"
    else:
        save_hash(path, current_hash)
        result = "ℹ️ No hash found. Current hash saved for future checks."

    result_text.set(result)
    last_result.set(result + f"\n\nHash:\n{current_hash}")

def export_result():
    if not file_path.get():
        messagebox.showwarning("Warning", "No file selected.")
        return

    result = last_result.get()
    if not result:
        messagebox.showwarning("Warning", "No result to export.")
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension=".txt", filetypes=[("Text Files", "*.txt")]
    )
    if save_path:
        with open(save_path, "w") as f:
            f.write("File Integrity Checker Report\n")
            f.write("=============================\n")
            f.write(f"File: {file_path.get()}\n\n")
            f.write(result + "\n")
        messagebox.showinfo("Exported", f"Result exported to:\n{save_path}")

def handle_drop(event):
    dropped = event.data.strip()
    if dropped.startswith("{") and dropped.endswith("}"):
        dropped = dropped[1:-1]  # Remove curly braces around path (spaces in filename)
    if os.path.isfile(dropped):
        file_path.set(dropped)
        result_text.set("📂 File dropped. Click 'Verify' to check integrity.")
    else:
        result_text.set("⚠️ Invalid file dropped.")

# --- TkinterDnD GUI Setup ---

app = TkinterDnD.Tk()  # Instead of tk.Tk()
app.title("🛡️ File Integrity Checker")
app.geometry("550x450")
app.resizable(False, False)

file_path = tk.StringVar()
result_text = tk.StringVar()
last_result = tk.StringVar()

app.title("🛡️ File Integrity Checker - by Tarun")

tk.Label(app, text="File Integrity Checker", font=("Helvetica", 18, "bold")).pack(pady=10)
tk.Label(app, text="Built using python by Tarun", font=("Helvetica", 10, "italic"), fg="gray").pack()


tk.Label(app, text="📥 Drag a file below or click Select File", font=("Helvetica", 10), fg="gray").pack()

# --- Drag-and-drop box ---
drop_box = tk.Label(app, text="⬇️ Drop File Here", relief="groove", bg="#f0f0f0", width=40, height=4)
drop_box.pack(pady=10)
drop_box.drop_target_register(DND_FILES)
drop_box.dnd_bind('<<Drop>>', handle_drop)

# --- Select + Verify ---
tk.Button(app, text="📂 Select File", command=select_file, font=("Helvetica", 12), bg="#007acc", fg="white", width=20).pack(pady=5)
tk.Label(app, textvariable=file_path, wraplength=500, font=("Helvetica", 10), fg="blue").pack(pady=5)
tk.Button(app, text="✅ Verify File", command=verify_file, font=("Helvetica", 12), bg="green", fg="white", width=20).pack(pady=10)

# --- Result Display ---
tk.Label(app, textvariable=result_text, wraplength=500, font=("Helvetica", 12), fg="black").pack(pady=10)

# --- Export & Clear Buttons ---
frame = tk.Frame(app)
frame.pack(pady=10)

tk.Button(frame, text="📝 Export Result", command=export_result, font=("Helvetica", 10), bg="#333", fg="white", width=20).grid(row=0, column=0, padx=5)
tk.Button(frame, text="🗑️ Clear Saved Hash", command=delete_saved_hash, font=("Helvetica", 10), bg="#b22222", fg="white", width=20).grid(row=0, column=1, padx=5)

app.mainloop()
