import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import yaml
import os

df = pd.read_csv('items_parsed.csv')

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

# === Logic to load template or blank ===
def use_template():
    print("Called use_template")
    item_name = selected_item.get()
    row = df[df['ItemName'] == item_name].iloc[0]
    root.show_item_screen(row)

def create_new():
    print("Called create_new")
    root.show_item_screen()

# Constants for slots and stats
def setup_item_gui(root):
    print("setting up item gui")

    # Define slots and stats at module scope
    root.SLOTS = ["MainHand", "OffHand", "Head", "Chest", "Legs", "Feet"]
    root.STATS = ["Armor", "ArmorToughness", "KnockbackResistance",
                  "Health", "AttackSpeed", "MovementSpeed", "Damage", "Luck"]
    # Storage for dynamic widgets
    root.slot_vars = {}
    root.slot_frames = {}
    root.slot_entries = {}

    # scrollable
    # 1. Create canvas + scrollbar
    canvas = tk.Canvas(root.item_frame)
    scrollbar = ttk.Scrollbar(root.item_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    # 2. Configure scrollable area
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # 3. Place canvas + scrollbar in layout
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # 4. Replace references: mount your GUI into scrollable_frame
    root.item_content_frame = scrollable_frame  # use this instead of root.item_frame in your GUI creation


    def show_item_screen(template_data=None):
        # Clear existing widgets
        for widget in root.winfo_children():
            widget.destroy()

        # --- Basic Item Fields ---
        fields = [
            ("Internal Name:", "name_entry", tk.Entry, "ItemName"),
            ("Minecraft ID:", "id_entry", tk.Entry, "Id"),
            ("Data (optional):", "data_entry", tk.Entry, "Data"),
            ("Display Name:", "display_entry", tk.Entry, "Display"),
            ("Lore (multi-line):", "lore_text", tk.Text, "Lore"),
            ("Enchantments (line per enchantment):", "enchantments_text", tk.Text, "Enchantments"),
            ("Unbreakable?", "unbreakable_var", tk.BooleanVar, "Option_Unbreakable"),
            ("Color (optional, RGB hex):", "color_entry", tk.Entry, "Option_Color"),
        ]

        row_index = 0
        for label_text, attr_name, widget_type, col_name in fields:
            tk.Label(root.item_content_frame, text=label_text).grid(
                row=row_index, column=0,
                sticky='e' if widget_type in (tk.Entry, tk.BooleanVar) else 'ne'
            )
            # instantiate
            if widget_type is tk.Text:
                widget = tk.Text(root.item_content_frame, width=40, height=4)
                widget.grid(row=row_index, column=1, sticky='w')
            elif widget_type is tk.BooleanVar:
                var = tk.BooleanVar(value=False)
                chk = tk.Checkbutton(root.item_content_frame, variable=var)
                chk.grid(row=row_index, column=1, sticky='w')
                widget = var
            else:
                widget = widget_type(root.item_content_frame, width=40)
                widget.grid(row=row_index, column=1, sticky='w')

            setattr(root.item_content_frame, attr_name, widget)
            # populate if template provided
            if template_data is not None:
                val = template_data.get(col_name) if isinstance(template_data, dict) else template_data[col_name]
                if widget_type is tk.Text and pd.notna(val):
                    widget.insert('1.0', val)
                elif widget_type is tk.BooleanVar and pd.notna(val):
                    widget.set(bool(val))
                elif widget_type is tk.Entry and pd.notna(val):
                    widget.insert(0, str(val))
            row_index += 1

        # Divider label
        tk.Label(root.item_content_frame, text="Equipment Slot Effects:", font=('Arial', 12, 'underline')).grid(
            row=row_index, column=0, columnspan=2, pady=(10, 5)
        )
        row_index += 1

        # --- Per-Slot Configurations ---
        for slot in root.SLOTS:
            var = tk.BooleanVar(value=False)
            root.item_content_frame.slot_vars[slot] = var
            chk = tk.Checkbutton(
                root.item_content_frame, text=slot, variable=var,
                command=lambda s=slot: toggle_slot_frame(s)
            )
            chk.grid(row=row_index, column=0, sticky='w', padx=(10,0))

            frame = tk.Frame(root.item_content_frame, relief='groove', bd=1)
            root.slot_frames[slot] = frame
            for si, stat in enumerate(root.STATS):
                tk.Label(frame, text=f"{stat}:").grid(row=si, column=0, sticky='e')
                ent = tk.Entry(frame, width=10)
                ent.grid(row=si, column=1, sticky='w')
                root.slot_entries[(slot, stat)] = ent

                # populate if template provided
                if template_data is not None:
                    col = f"{slot}_{stat}"
                    val = template_data.get(col) if isinstance(template_data, dict) else template_data.get(col, None)
                    if pd.notna(val):
                        var.set(True)
                        ent.insert(0, str(val))

            frame.grid(row=row_index, column=1, sticky='w', padx=(0,10))
            frame.grid_remove()

            # if any values were set, show frame
            if template_data is not None and var.get():
                toggle_slot_frame(slot)

            row_index += 1

        # Save Button at the bottom
        save_btn = tk.Button(root, text="Save Item", command=save_to_yaml)
        save_btn.grid(row=row_index, column=0, columnspan=2, pady=(15,0))

    def save_to_yaml():
        name = root.name_entry.get()
        if not name:
            messagebox.showerror("Error", "Item name is required!")
            return

        try:
            def get_text_lines(widget):
                return [line.strip() for line in widget.get("1.0", tk.END).strip().splitlines() if line.strip()]

            # Required elements
            item_data = {
                'Id': root.id_entry.get(),
                'Display': root.display_entry.get(),
                'Lore': get_text_lines(root.lore_text),
            }

            if root.data_entry.get():
                item_data['Data'] = int(root.data_entry.get())
            
            if len(root.enchantments_text):
                item_data['Enchantments'] = get_text_lines(root.enchantments_text)

            if root.unbreakable_var.get():
                item_data['Options'] = {'Unbreakable': True}

            color_val = root.color_entry.get().strip()
            if len(color_val):
                if 'Options' not in item_data:
                    item_data['Options'] = {'Color': color_val}
                else:
                    item_data['Options']['Color'] = color_val

            # Gather attributes
            attributes = {}
            for slot in root.SLOTS:
                if root.slot_vars[slot].get():
                    slot_data = {}
                    for stat in root.STATS:
                        val = root.slot_entries[(slot, stat)].get()
                        if val:
                            try:
                                slot_data[stat] = str(val)
                            except ValueError:
                                raise ValueError(f"Invalid number for {slot}_{stat}: '{val}'")
                    if slot_data:
                        attributes[slot] = slot_data

            if attributes:
                item_data['Attributes'] = attributes

            # Write to file
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
                yaml.dump(existing, f, sort_keys=True)

            messagebox.showinfo("Saved", f"Item '{name}' saved to {filename}!")

        except Exception as e:
            messagebox.showerror("Save Failed", f"An error occurred while saving:\n{str(e)}")

    def toggle_slot_frame(slot):
        frame = root.slot_frames[slot]
        if root.slot_vars[slot].get():
            frame.grid()
        else:
            frame.grid_remove()

    # Attach functions to root so they can be called externally
    root.show_item_screen = show_item_screen
    root.toggle_slot_frame = toggle_slot_frame


# Example usage when creating your application:
if __name__ == '__main__':
    root = tk.Tk()
    root.title("RPG Item Creator")

    item_names = list(df['ItemName'])
    selected_item = tk.StringVar()

    setup_item_gui(root)
    show_start_screen()
    root.mainloop()
