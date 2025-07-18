import pandas as pd
import numpy as np

df = pd.read_csv('ellen_format.csv')

def get_user_input():
    fil_type = input("Enter item type (or press Enter to skip): ").strip() or None
    fil_class = input("Enter item class (or press Enter to skip): ").strip() or None
    rarity = input("Enter rarity (or press Enter to skip): ").strip() or None

    return fil_type, fil_class, rarity

def random_item(fil_type=None, fil_class=None, rarity=None):
    filtered = df
    if fil_type:
        filtered = filtered[filtered['Type'] == fil_type]
    if fil_class:
        filtered = filtered[filtered['Class'] == fil_class]
    if rarity:
        filtered = filtered[filtered['Rarity'] == rarity]
    return filtered.sample(1)

# Get user input
fil_type, fil_class, rarity = get_user_input()


# Call function with user input
item = random_item(fil_type, fil_class, rarity).iloc[[0]]

print("Your randomly selected item is: \n\t", item)