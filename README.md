# Introduction

This repository contains Python tools for Ian's RPG Minecraft server.

# Item Creation
Items are made using the Mythic Mobs plugin framework. All items that can be created are stored in items.yml, which should be regularly updated.

Here is an explanation of the different fields an item can have.

```
ItemName: Required. Camelcase name for the item used as ID.

  Id: The base minecraft item, e.g. IRON_SWORD.

  Display: The displayed name of the item.

  Attributes: Attributes come in one of [All, MainHand, OffHand, Head, Chest, Legs, Feet]. They can be either raw numbers (+30, -15) or percentages (+45%).

    MainHand:
      Armor: Sets the amount of armor. 1 armor is equal to 0.5 armor plates. Vanilla caps the amount to 30.

      ArmorToughness: Armor becomes less effective for higher damage values, reducing the damage by smaller and smaller percentages. Armor toughness mitigates this behavior to a degree.

      AttackSpeed: Determines the recharge rate of a fully charged attack.

      Damage: Sets the damage dealt by melee attacks. 1 damage equals to 0.5 hearts of damage dealt (without armor).

      Health: The maximum health modifier the user can have when either holding or wearing the item. 1 health equals to 0.5 hearts.

      KnockbackResistance: Sets the horizontal scale knockback resisted from attacks.

      Luck: Sets the amount of luck modifier of the item. This modifier affects the result of loot tables and also the mob drops.

      MovementSpeed: Sets the movement speed modifier of the item.

  Data (optional): Value used for determining type, e.g. for differently colored leather? 

  Enchantments: Each enchantment is listed on its own line, as the ID of the enchantment then its level.

  - DAMAGE:74

  - KNOCKBACK:15

  Lore: The text of the item. 

  - Lots of Lore...

  - '[Brawler, Melee]'

  Options (optional): 

    Color: probably for like leather dying?

    Unbreakable: True/False. Default is false. If true, item doesn't take damage 
    ```