import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
import yaml
import os

SLOTS = ["MainHand", "OffHand", "Head", "Chest", "Legs", "Feet"]
STATS = ["Armor", "ArmorToughness", "KnockbackResistance",
         "Health", "AttackSpeed", "MovementSpeed", "Damage", "Luck"]


df = pd.read_csv('items_parsed.csv', index_col="ItemName")

# === Step 1: Start screen ===
def show_start_screen():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Select an existing item:").grid(row=0, column=0, pady=10, padx=10)

    selected_item.set(item_names[0])
    dropdown = ttk.OptionMenu(root, selected_item, item_names[0], *item_names)
    dropdown.grid(row=0, column=1)

    use_template_btn = tk.Button(root, text="Use Template", command=use_template)
    use_template_btn.grid(row=1, column=0, pady=10)

    new_item_btn = tk.Button(root, text="Create New Item", command=create_new)
    new_item_btn.grid(row=1, column=1)

# === Step 2: Go to item creation screen ===
def show_item_screen(template_data=None):
    for widget in root.winfo_children():
        widget.destroy()

    # Fields to create as (Label text, attribute name, widget class)
    fields = [
        ("Name:", "name_entry", tk.Entry),
        ("Id:", "id_entry", tk.Entry),
        ("Data:", "data_entry", tk.Entry),
        ("Display:", "display_entry", tk.Entry),
        ("Lore:", "lore_text", tk.Text),
        ("Enchantments (e.g. DAMAGE_ALL:5):", "enchantments_text", tk.Text),
        ("Attack Speed:", "attack_speed_entry", tk.Entry),
        ("Health:", "health_entry", tk.Entry),
        ("Movement Speed:", "movement_speed_entry", tk.Entry),
        ("Armor:", "armor_entry", tk.Entry),
        ("Armor Toughness:", "armor_toughness_entry", tk.Entry),
        ("Damage:", "damage_entry", tk.Entry),
    ]

    for i, (label_text, attr_name, widget_class) in enumerate(fields):
        tk.Label(root, text=label_text).grid(row=i, column=0, sticky='ne' if widget_class is tk.Text else 'e')
        widget = widget_class(root, height=5, width=30) if widget_class is tk.Text else widget_class(root, width=30)
        widget.grid(row=i, column=1)
        setattr(root, attr_name, widget)

    # Save button
    tk.Button(root, text="Save to YAML", command=save_to_yaml).grid(row=len(fields), column=0, columnspan=2, pady=10)

    # Fill from template
    if template_data is not None:
        field_map = {
            'ItemName': 'name_entry',
            'Id': 'id_entry',
            'Data': 'data_entry',
            'Display': 'display_entry',
        }
        for key, attr in field_map.items():
            widget = getattr(root, attr)
            widget.delete(0, tk.END)
            widget.insert(0, str(template_data.get(key, "")))

# === Logic to load template or blank ===
def use_template():
    item_name = selected_item.get()
    row = df.loc[item_name]
    show_item_screen(row)

def create_new():
    show_item_screen()


def save_to_yaml():
    name = root.name_entry.get()
    if not name:
        messagebox.showerror("Error", "Item name is required!")
        return

    try:
        # Helper to get text area lines
        def get_text_lines(widget):
            return [line.strip() for line in widget.get("1.0", tk.END).strip().splitlines()]

        # Attributes to fetch from entries
        attr_fields = [
            "attack_speed_entry",
            "health_entry",
            "movement_speed_entry",
            "armor_entry",
            "armor_toughness_entry",
            "damage_entry"
        ]

        item_data = {
            'Id': root.id_entry.get(),
            'Data': int(root.data_entry.get() or 0),  
            'Display': root.display_entry.get(),
            'Lore': get_text_lines(root.lore_text),
            'Enchantments': get_text_lines(root.enchantments_text),
            'Attributes': {
                'MainHand': {
                    attr.replace("_entry", "").title().replace("_", ""): getattr(root, attr).get()
                    for attr in attr_fields
                }
            }
        }

        filename = "items.yml"
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                try:
                    existing = yaml.safe_load(f) or {}
                except yaml.YAMLError:
                    existing = {}
        else:
            existing = {}

        existing[name] = item_data

        with open(filename, 'w', encoding='utf-8') as f:
            yaml.dump(existing, f, sort_keys=False)

        messagebox.showinfo("Saved", f"Item '{name}' saved to {filename}!")

    except Exception as e:
        messagebox.showerror("Save Failed", f"An error occurred while saving:\n{str(e)}")


# === Main window ===
root = tk.Tk()
root.title("RPG Item Creator")

item_names = list(df.index)
selected_item = tk.StringVar()

show_start_screen()
root.mainloop()