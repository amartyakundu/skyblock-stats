def truncate_two_decimals(amount, unit):
    # Cut off after 2 decimal places without rounding up (999.999 -> 999.99)
    # Uses whole numbers so no tiny decimal errors sneak in
    hundredths = int(amount) // (unit // 100)
    return hundredths / 100


def format_money(amount):

    if amount >= 1_000_000_000:
        return f"{truncate_two_decimals(amount, 1_000_000_000):.2f}B"

    elif amount >= 1_000_000:
        return f"{truncate_two_decimals(amount, 1_000_000):.2f}M"

    elif amount >= 1_000:
        return f"{truncate_two_decimals(amount, 1_000):.2f}K"

    return f"{int(amount)}"
def format_level(experience):

    level = experience // 100
    progress = experience % 100

    return f"{level}.{progress:02d}"


def get_skill_progress(skill_xp, skill_levels):
    previous_total_xp = 0

    for level_data in skill_levels:
        level = level_data["level"]
        total_xp_for_level = level_data["totalExpRequired"]

        if skill_xp < total_xp_for_level:
            xp_into_level = skill_xp - previous_total_xp
            xp_needed_for_next_level = total_xp_for_level - previous_total_xp

            return level - 1, xp_into_level, xp_needed_for_next_level, 0

        previous_total_xp = total_xp_for_level

    max_level = skill_levels[-1]["level"]
    overflow_xp = skill_xp - previous_total_xp

    return max_level, 0, 0, overflow_xp


def remove_minecraft_color_codes(text):
    clean_text = ""
    skip_next_character = False

    for character in str(text):
        if skip_next_character:
            skip_next_character = False

        elif character == "§":
            skip_next_character = True

        else:
            clean_text += character

    return clean_text

def get_item_rarity(raw_item_name):  
    rarity_colors = {
        "§f": "Common",
        "§a": "Uncommon",
        "§9": "Rare",
        "§5": "Epic",
        "§6": "Legendary",
        "§d": "Mythic",
        "§b": "Divine",
        "§c": "Special"
    }

    color_code = str(raw_item_name)[:2]

    return rarity_colors.get(color_code, "Unknown")