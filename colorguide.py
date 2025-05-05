import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

PRESETS_FILE = "presets.json"

def load_presets():
    if os.path.exists(PRESETS_FILE):
        with open(PRESETS_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

def save_presets(presets):
    with open(PRESETS_FILE, "w") as f:
        json.dump(presets, f, indent=2)

def rgb_to_decimal(r, g, b):
    return round(r / 255, 3), round(g / 255, 3), round(b / 255, 3)

class ColorConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RGB + HEX → Decimal Converter")

        self.presets = load_presets()

        self.create_widgets()
        self.update_preview()

    def create_widgets(self):
        # Preset Choice
        preset_label = tk.Label(self.root, text="Choose a preset:")
        preset_label.pack()

        self.preset_var = tk.StringVar()
        self.preset_menu = ttk.Combobox(self.root, textvariable=self.preset_var, values=list(self.presets.keys()))
        self.preset_menu.pack()
        self.preset_menu.bind("<<ComboboxSelected>>", self.apply_preset)

        # RGB-Slider
        self.sliders = {}
        for color in ("red", "green", "blue"):
            label = tk.Label(self.root, text=color)
            label.pack()
            slider = tk.Scale(self.root, from_=0, to=255, orient="horizontal", command=lambda e: self.update_preview())
            slider.pack(fill="x")
            self.sliders[color] = slider

        # Preview
        self.preview = tk.Label(self.root, text="  preview  ", bg="#000000", fg="white")
        self.preview.pack(pady=10, fill="x")

        # Output
        self.output = tk.Text(self.root, height=4, width=40)
        self.output.pack()

 # HEX-Colorcode
        hex_frame = tk.Frame(self.root)
        hex_frame.pack(pady=5)

        tk.Label(hex_frame, text="HEX-Color (#rrggbb):").pack(side="left")
        self.hex_entry = tk.Entry(hex_frame)
        self.hex_entry.pack(side="left")
        hex_button = tk.Button(hex_frame, text="import", command=self.apply_hex)
        hex_button.pack(side="left")

        # Add Preset 
        self.new_preset_frame = tk.Frame(self.root)
        self.new_preset_frame.pack(pady=5)

        tk.Label(self.new_preset_frame, text="Presetname:").pack(side="left")
        self.new_preset_entry = tk.Entry(self.new_preset_frame)
        self.new_preset_entry.pack(side="left")

        save_button = tk.Button(self.new_preset_frame, text="Save", command=self.save_preset)
        save_button.pack(side="left", padx=5)

        # Copy
        copy_button = tk.Button(self.root, text="Copy values", command=self.copy_to_clipboard)
        copy_button.pack(pady=5)

        # Delete
        delete_button = tk.Button(self.root, text="Delete Preset", command=self.delete_preset)
        delete_button.pack(pady=5)

    def apply_preset(self, event):
        rgb = self.presets[self.preset_var.get()]
        self.sliders["red"].set(rgb[0])
        self.sliders["green"].set(rgb[1])
        self.sliders["blue"].set(rgb[2])
        self.update_preview()

    def update_preview(self):
        r = self.sliders["red"].get()
        g = self.sliders["green"].get()
        b = self.sliders["blue"].get()

        color_hex = f"#{r:02x}{g:02x}{b:02x}"
        self.preview.config(bg=color_hex)

        red, green, blue = rgb_to_decimal(r, g, b)
        decimal = f"red: {red}\ngreen: {green}\nblue: {blue}"
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, decimal)

    def apply_hex(self):
        hex_value = self.hex_entry.get().strip().lstrip("#")
        if len(hex_value) != 6:
            messagebox.showerror("error", "Please enter a valid HEX-Code (e. g. #ff9900)")
            return
        try:
            r = int(hex_value[0:2], 16)
            g = int(hex_value[2:4], 16)
            b = int(hex_value[4:6], 16)
        except ValueError:
            messagebox.showerror("error", "invalid HEX-Code.")
            return

        self.sliders["red"].set(r)
        self.sliders["green"].set(g)
        self.sliders["blue"].set(b)
        self.update_preview()

    def copy_to_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.output.get("1.0", tk.END).strip())
        self.root.update()

    def save_preset(self):
        name = self.new_preset_entry.get().strip()
        if not name:
            return
        r = self.sliders["red"].get()
        g = self.sliders["green"].get()
        b = self.sliders["blue"].get()
        self.presets[name] = [r, g, b]
        save_presets(self.presets)
        self.preset_menu["values"] = list(self.presets.keys())
        self.new_preset_entry.delete(0, tk.END)

    def delete_preset(self):
        name = self.preset_var.get()
        if name in self.presets:
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete preset '{name}' ?")
            if confirm:
                del self.presets[name]
                save_presets(self.presets)
                self.preset_menu["values"] = list(self.presets.keys())
                self.preset_var.set("")
                self.output.delete("1.0", tk.END)
                self.preview.config(bg="#000000")


if __name__ == "__main__":
    root = tk.Tk()
    app = ColorConverterApp(root)
    root.mainloop()
