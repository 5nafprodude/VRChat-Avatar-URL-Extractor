import re
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, colorchooser
import sys
import subprocess

# --- Dependency Installation ---
# This part is optional but useful for a standalone script.
# For a PyInstaller build, this part can be removed as the dependency is bundled.
try:
    import tkinterdnd2 as tkdnd
except ImportError:
    tkdnd = None

def install_missing_dependencies():
    """Checks for and installs required Python packages."""
    required_packages = ['tkinterdnd2']
    for package in required_packages:
        try:
            if package == 'tkinterdnd2' and not tkdnd:
                raise ImportError
            __import__(package.lower().split(' ')[0])
            print(f"Package '{package}' is already installed.")
        except ImportError:
            print(f"Package '{package}' not found. Installing...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"Successfully installed '{package}'.")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Installation Error", f"Failed to install '{package}'. Please install it manually using 'pip install {package}'.\nError: {e}")
                sys.exit(1)
            except Exception as e:
                messagebox.showerror("Installation Error", f"An unexpected error occurred during installation of '{package}'.\nError: {e}")
                sys.exit(1)

install_missing_dependencies()

# --- Main Application Logic ---
class DragDropTk(tkdnd.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dnd_bind('<<Drop>>', self.drop_handler)

    def drop_handler(self, event):
        filepath = event.data.strip('{}')
        if os.path.isfile(filepath):
            process_file(filepath)

if tkdnd:
    root = DragDropTk()
    root.drop_target_register(tkdnd.DND_FILES)
else:
    root = tk.Tk()
    messagebox.showwarning(
        "Warning",
        "tkinterdnd2 not found. Drag and drop functionality will not be available.\n"
        "To install, run: pip install tkinterdnd2"
    )

APP_TITLE = "VRChat Avatar URL Extractor"
dark_mode = True
custom_bg_color = None

# New setting for auto-copy and notification
auto_copy_var = tk.BooleanVar(value=False)
show_copy_notification_var = tk.BooleanVar(value=True)

# Icon paths
local_icon_path = "app_icon.ico"
system_root = os.environ.get('SystemRoot')
system_icon_path = os.path.join(system_root, 'System32', 'shell32.dll') + ",0"

def extract_avatar_id(filepath):
    """Extract avatar ID from the file name using a regular expression."""
    filename = os.path.basename(filepath)
    match = re.search(r"(avtr_[0-9a-fA-F-]+)", filename)
    return match.group(1) if match else None

def process_file(filepath):
    """Processes a selected or dropped file to extract and display the avatar URL."""
    avtr_id = extract_avatar_id(filepath)
    if not avtr_id:
        messagebox.showerror("Error", "No avatar ID found in the file name.")
        return

    avatar_url = f"https://vrchat.com/home/avatar/{avtr_id}"
    file_label_var.set(f"Selected: {os.path.basename(filepath)}")
    url_entry.delete(0, tk.END)
    url_entry.insert(0, avatar_url)

    if auto_copy_var.get():
        copy_url()

def select_file():
    """Opens a file dialog for the user to select a VRChat file."""
    filepath = filedialog.askopenfilename(
        title="Select VRChat File",
        filetypes=[("VRChat Files", "*.prefab *.unity3d *.vrca"), ("All Files", "*.*")]
    )
    if filepath:
        process_file(filepath)

def copy_url():
    """Copies the generated URL to the clipboard, with an optional notification."""
    url = url_entry.get()
    if url and url != url_placeholder:
        root.clipboard_clear()
        root.clipboard_append(url)
        
        # New conditional check for the notification
        if show_copy_notification_var.get():
            messagebox.showinfo("Copied", "URL copied to clipboard!")
    else:
        messagebox.showwarning("Warning", "No URL to copy.")

def clear_selection():
    """Resets the UI to its initial state."""
    file_label_var.set("No file selected")
    url_entry.delete(0, tk.END)
    add_placeholder()

def add_placeholder(event=None):
    """Adds placeholder text to the entry widget if it's empty."""
    if not url_entry.get():
        url_entry.insert(0, url_placeholder)
        url_entry.configure(foreground=theme_colors["hint_fg"])

def remove_placeholder(event=None):
    """Removes placeholder text from the entry widget."""
    if url_entry.get() == url_placeholder:
        url_entry.delete(0, tk.END)
        url_entry.configure(foreground=theme_colors["entry_fg"])

# --- Theming Functions ---
def hex_to_rgb(hex_color):
    """Converts a hex color string to an RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb_color):
    """Converts an RGB tuple to a hex color string."""
    return f'#{rgb_color[0]:02x}{rgb_color[1]:02x}{rgb_color[2]:02x}'

def darken_color(hex_color, factor=0.8):
    """Darkens a hex color by a given factor."""
    rgb_color = hex_to_rgb(hex_color)
    darkened_rgb = tuple(int(c * factor) for c in rgb_color)
    return rgb_to_hex(darkened_rgb)

def get_luminance(rgb_color):
    """Calculates the perceived brightness (luminance) of an RGB color."""
    r, g, b = (c / 255.0 for c in rgb_color)
    return 0.299 * r + 0.587 * g + 0.114 * b

def apply_theme():
    """Applies either the dark or light theme or custom color to the UI."""
    global dark_mode, custom_bg_color, theme_colors

    dark_theme_colors = {
        "bg": "#2c3e50", "fg": "#ecf0f1", "header_bg": "#34495e", "header_fg": "#ffffff",
        "button_bg": "#3498db", "button_fg": "white", "active_button_bg": "#2980b9",
        "entry_bg": "#34495e", "entry_fg": "#ecf0f1", "hint_fg": "#bdc3c7"
    }
    light_theme_colors = {
        "bg": "#ecf0f1", "fg": "#2c3e50", "header_bg": "#ffffff", "header_fg": "#2c3e50",
        "button_bg": "#2ecc71", "button_fg": "white", "active_button_bg": "#27ae60",
        "entry_bg": "white", "entry_fg": "#2c3e50", "hint_fg": "#7f8c8d"
    }

    if dark_mode:
        theme_colors = dark_theme_colors
    else:
        theme_colors = light_theme_colors

    if custom_bg_color:
        root_bg_color = custom_bg_color
        custom_rgb = hex_to_rgb(root_bg_color)
        luminance = get_luminance(custom_rgb)
        button_fg_color = "white" if luminance < 0.5 else "black"
        button_bg_color = darken_color(root_bg_color, factor=0.8)
        active_button_bg_color = darken_color(root_bg_color, factor=0.6)
        
        theme_colors["button_bg"] = button_bg_color
        theme_colors["button_fg"] = button_fg_color
        theme_colors["active_button_bg"] = active_button_bg_color
        theme_colors["header_bg"] = button_bg_color
        theme_colors["header_fg"] = button_fg_color
    else:
        root_bg_color = theme_colors["bg"]

    luminance = get_luminance(hex_to_rgb(root_bg_color))
    fg_color = "black" if luminance > 0.5 else "white"

    style.configure("TFrame", background=root_bg_color)
    style.configure("TLabel", background=root_bg_color, foreground=fg_color)
    style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=10, background=theme_colors["button_bg"], foreground=theme_colors["button_fg"], borderwidth=0)
    style.map("TButton", background=[("active", theme_colors["active_button_bg"])])
    style.configure("TEntry", font=("Segoe UI", 11), padding=12, fieldbackground=theme_colors["entry_bg"], borderwidth=0, relief="flat")
    style.configure("Header.TFrame", background=theme_colors["header_bg"])
    style.configure("Header.TLabel", font=("Segoe UI", 24, "bold"), foreground=theme_colors["header_fg"], background=theme_colors["header_bg"])

    faded_bg_rgb = tuple(int(c * 0.7) for c in hex_to_rgb(root_bg_color))
    faded_bg_hex = "#%02x%02x%02x" % faded_bg_rgb
    style.configure("Faded.TFrame", background=faded_bg_hex, relief="flat", borderwidth=0)

    title_label.configure(style="Header.TLabel")
    file_label.configure(style="TLabel", font=("Segoe UI", 10, "italic"), foreground=theme_colors["hint_fg"], background=faded_bg_hex)
    hint_label.configure(style="TLabel", font=("Segoe UI", 10), foreground=theme_colors["hint_fg"], background=faded_bg_hex)
    settings_title_label.configure(style="TLabel", font=("Segoe UI", 18, "bold"), foreground=fg_color)
    credits_label.configure(style="TLabel", foreground=fg_color, background=root_bg_color)
    root.configure(bg=root_bg_color)

    if url_entry.get() == url_placeholder:
        url_entry.configure(foreground=theme_colors["hint_fg"])
    else:
        url_entry.configure(foreground=theme_colors["entry_fg"])

# --- UI Layout and Functions ---
def change_background_color_dialog():
    """Opens a color chooser and sets the background color."""
    global custom_bg_color
    color_code = colorchooser.askcolor(title="Choose Background Color")[1]
    if color_code:
        custom_bg_color = color_code
        apply_theme()

def show_settings():
    """Switches the view from the main UI to the settings UI."""
    main_frame.place_forget()
    settings_frame.place(relx=0.5, rely=0.5, anchor="center")
    settings_frame.lift()

def show_main_ui():
    """Switches the view from the settings UI back to the main UI."""
    settings_frame.place_forget()
    main_frame.place(relx=0.5, rely=0.5, anchor="center")
    main_frame.lift()

def toggle_theme():
    """Switches between dark and light themes."""
    global dark_mode, custom_bg_color
    dark_mode = not dark_mode
    custom_bg_color = None
    apply_theme()
    add_placeholder()

# --- GUI Setup ---
root.title(APP_TITLE)
root.geometry("700x400")
root.minsize(600, 300)

try:
    if os.path.exists(local_icon_path):
        root.iconbitmap(local_icon_path)
    else:
        root.iconbitmap(system_icon_path)
except tk.TclError:
    pass

style = ttk.Style()
style.theme_use('clam')
theme_colors = {}

# Main UI Frame
main_frame = ttk.Frame(root, padding="40 40 40 40")
main_frame.place(relx=0.5, rely=0.5, anchor="center")

header_frame = ttk.Frame(main_frame, padding="15 15 15 15", style="Header.TFrame")
header_frame.pack(fill="x", pady=(0, 25))
title_label = ttk.Label(header_frame, text="🖋️  " + APP_TITLE, style="Header.TLabel")
title_label.pack()

file_label_frame = ttk.Frame(main_frame, style="Faded.TFrame")
file_label_frame.pack(pady=(10, 10))
file_label_var = tk.StringVar(value="No file selected")
file_label = ttk.Label(file_label_frame, textvariable=file_label_var)
file_label.pack(padx=10, pady=5)

url_placeholder = "Avatar URL will appear here..."
url_entry = ttk.Entry(main_frame, justify="center")
url_entry.bind("<FocusIn>", remove_placeholder)
url_entry.bind("<FocusOut>", add_placeholder)
url_entry.pack(fill="x", pady=10)

button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=15)
ttk.Button(button_frame, text="Select File", command=select_file).pack(side="left", padx=5)
ttk.Button(button_frame, text="Copy URL", command=copy_url).pack(side="left", padx=5)

utility_button_frame = ttk.Frame(main_frame)
utility_button_frame.pack()
ttk.Button(utility_button_frame, text="Clear", command=clear_selection).pack(side="left", padx=5)
ttk.Button(utility_button_frame, text="Settings", command=show_settings).pack(side="left", padx=5)

hint_label_frame = ttk.Frame(main_frame, style="Faded.TFrame")
hint_label_frame.pack(pady=(15, 0))
hint_label = ttk.Label(hint_label_frame, text="💡 Tip: Drag and drop a file anywhere on the window.")
hint_label.pack(padx=10, pady=5)

# Settings UI Frame
settings_frame = ttk.Frame(root, padding="40 40 40 40")
settings_frame.place(relx=0.5, rely=0.5, anchor="center")

settings_title_label = ttk.Label(settings_frame, text="Customize Appearance")
settings_title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

ttk.Button(settings_frame, text="Change Background Color", command=change_background_color_dialog).grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")
ttk.Button(settings_frame, text="Toggle Dark/Light Mode", command=toggle_theme).grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")

ttk.Checkbutton(settings_frame, text="Auto-copy URL to clipboard", variable=auto_copy_var).grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")

# New checkbox for the notification
ttk.Checkbutton(settings_frame, text="Show 'URL Copied!' notification", variable=show_copy_notification_var).grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")

back_button = ttk.Button(settings_frame, text="Back", command=show_main_ui)
back_button.grid(row=5, column=0, columnspan=2, pady=(20, 0), sticky="ew")

# UPDATED: Credit line now says "Made by Naf"
credits_label = ttk.Label(settings_frame, text="Made by Naf", font=("Segoe UI", 9, "italic"))
credits_label.grid(row=6, column=0, columnspan=2, pady=(20, 0))

# Initial theme application and UI display
apply_theme()
add_placeholder()
show_main_ui()

root.mainloop()