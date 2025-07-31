import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import threading
from content_down import download_content  
def read_content_list():
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_path, "all_contents.txt")
        with open(file_path, "r", encoding="utf-8") as f:
            return [content.strip() for content in f.read().split(',') if content.strip()]
    except Exception as e:
        print(f"Error loading content list: {e}")
        return []

def update_suggestions(event=None):
    query = content_entry_var.get().lower()
    suggestion_listbox.delete(0, tk.END)
    if query:
        matches = [m for m in all_contents if query in m.lower()]
        for match in matches[:10]:
            suggestion_listbox.insert(tk.END, match)
        suggestion_frame.grid(row=2, column=1, sticky="ew", padx=10)
    else:
        suggestion_frame.grid_remove()

def select_from_listbox(event=None):
    if suggestion_listbox.curselection():
        selected = suggestion_listbox.get(suggestion_listbox.curselection())
        content_entry_var.set(selected)
        suggestion_frame.grid_remove()

def start_download():
    content = content_entry_var.get()
    quality = quality_var.get()
    if not content:
        messagebox.showerror("Error", "Please enter a content name.")
        return
    if quality == "Select Quality":
        messagebox.showerror("Error", "Please select quality.")
        return
    messagebox.showinfo("Download", f"Starting download for:\n{content} ({quality})")
    threading.Thread(target=download_content, args=(content, quality), daemon=True).start()
    # Your download logic here

all_contents = read_content_list()

# --- UI SETUP ---
root = tk.Tk()
root.title("Velocontent Downloader")
root.geometry("500x350")
root.resizable(False, False)
root.configure(bg="#f9f9f9")

# --- Fonts & Styling ---
LABEL_FONT = ("Segoe UI", 11)
ENTRY_FONT = ("Segoe UI", 11)
TITLE_FONT = ("Segoe UI", 15, "bold")

# --- Main Frame ---
main_frame = tk.Frame(root, bg="#f9f9f9")
main_frame.pack(pady=20, padx=20, fill="both", expand=True)

# --- Title ---
tk.Label(main_frame, text="Velocontent Downloader", font=TITLE_FONT, bg="#f9f9f9", fg="#333").grid(row=0, column=0, columnspan=2, pady=(0, 15))

# --- content Name ---
tk.Label(main_frame, text="content Name:", font=LABEL_FONT, bg="#f9f9f9").grid(row=1, column=0, sticky="w")
content_entry_var = tk.StringVar()
content_entry = tk.Entry(main_frame, textvariable=content_entry_var, font=ENTRY_FONT, width=30)
content_entry.grid(row=1, column=1, sticky="ew", padx=10)
content_entry.bind("<KeyRelease>", update_suggestions)

# --- Suggestion Listbox ---
suggestion_frame = tk.Frame(main_frame, bg="#f9f9f9")
suggestion_listbox = tk.Listbox(suggestion_frame, height=5, font=("Segoe UI", 10), activestyle='dotbox')
suggestion_listbox.pack(fill="both", expand=True)
suggestion_listbox.bind("<<ListboxSelect>>", select_from_listbox)
suggestion_frame.grid_remove()  # initially hidden

# --- Quality ---
tk.Label(main_frame, text="Select Quality:", font=LABEL_FONT, bg="#f9f9f9").grid(row=3, column=0, sticky="w", pady=(15, 0))
quality_var = tk.StringVar(value="Select Quality")
quality_dropdown = ttk.Combobox(main_frame, textvariable=quality_var, font=ENTRY_FONT,
                                 values=["480p", "720p", "1080p", "HQ 1080p"], state="readonly")
quality_dropdown.grid(row=3, column=1, sticky="ew", padx=10, pady=(15, 0))

# --- Download Button ---
download_btn = tk.Button(main_frame, text="Download 🎬", font=("Segoe UI", 11, "bold"),
                         bg="#4CAF50", fg="white", padx=10, pady=6,
                         command=start_download)
download_btn.grid(row=4, column=0, columnspan=2, pady=25, ipadx=5)

# Make columns responsive
main_frame.columnconfigure(1, weight=1)

root.mainloop()
