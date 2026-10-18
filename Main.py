import json
import httpx

from formatting import (
    format_money,
    format_level,
    get_skill_progress,
    remove_minecraft_color_codes,
    get_item_rarity,
)
from config import API_KEY
from inventory import decode_inventory_data
from dungeons import format_dungeons

def get_minecraft_uuid(client, username):
    #mojang api
    mojang_url = f"https://api.minecraftservices.com/minecraft/profile/lookup/name/{username}"
    mojang_response = client.get(mojang_url)
    if mojang_response.status_code == 200:
        mojang_data = mojang_response.json()
        return mojang_data["id"]
    elif mojang_response.status_code == 404:
        print("Player not found.")
    else:
        print(f"Mojang API Error: {mojang_response.status_code}")
    return None
def get_hypixel_data(client, uuid):
    # hypixel API
    hypixel_url = f"https://api.hypixel.net/v2/skyblock/profiles?uuid={uuid}"
    headers = {
        "API-Key": API_KEY
    }
    hypixel_response = client.get(hypixel_url, headers=headers)
    if hypixel_response.status_code != 200:
        print(f"Hypixel API Error: {hypixel_response.status_code}")
        return None
    return hypixel_response.json()
def get_skills_data(client):
    #skills api
    skills_url = "https://api.hypixel.net/v2/resources/skyblock/skills"
    skills_response = client.get(skills_url)
    if skills_response.status_code != 200:
        print(f"Skills API Error: {skills_response.status_code}")
        return None
    return skills_response.json()["skills"]
def get_selected_profile(hypixel_data):
    #active profile finder
    for profile in hypixel_data.get("profiles") or []:
        if profile.get("selected"):
            return profile
    return None
def print_profile_info(selected_profile, uuid):
    #profile info
    print(f"Selected Profile: {selected_profile['cute_name']}")
    player = selected_profile["members"][uuid]
    profile_type = selected_profile.get("game_mode", "Normal")
    level = player["leveling"]["experience"]
    purse = player["currencies"]["coin_purse"]
    bank = player["profile"]["bank_account"]
    print(f"Profile Type: {profile_type}")
    print(f"SkyBlock Level: {format_level(level)}")
    print(f"Purse: {format_money(purse)}")
    print(f"Bank: {format_money(bank)}")
    fairy_souls = player["fairy_soul"]["total_collected"]
    print(f"Total Fairy Souls Collected: {fairy_souls}")
    return player
def print_skills(player, skills_data):
    #skills info
    print()
    print("Skills:")
    skill_names = [
        ("FARMING", "SKILL_FARMING"),
        ("MINING", "SKILL_MINING"),
        ("COMBAT", "SKILL_COMBAT"),
        ("FORAGING", "SKILL_FORAGING"),
        ("FISHING", "SKILL_FISHING"),
        ("ENCHANTING", "SKILL_ENCHANTING"),
        ("ALCHEMY", "SKILL_ALCHEMY"),
        ("CARPENTRY", "SKILL_CARPENTRY"),
        ("RUNECRAFTING", "SKILL_RUNECRAFTING"),
        ("SOCIAL", "SKILL_SOCIAL"),
        ("TAMING", "SKILL_TAMING"),
        ("HUNTING", "SKILL_HUNTING")
    ]
    player_skill_xp = player["player_data"]["experience"]
    for skill_name, xp_key in skill_names:
        skill_xp = player_skill_xp.get(xp_key, 0)
        skill_info = skills_data[skill_name]
        skill_level, current_xp, xp_needed, overflow_xp = get_skill_progress(
            skill_xp,
            skill_info["levels"]
        )
        display_name = skill_info["name"]
        if skill_level == skill_info["maxLevel"]:
            print(
                f"{display_name} {skill_level} | "
                f"Overflow: {overflow_xp:,.0f} XP"
            )
        else:
            print(
                f"{display_name} {skill_level} | "
                f"{current_xp:,.0f}/{xp_needed:,.0f} XP"
            )
def print_dungeons_info(player):
    #dungeons info
    print()
    print(format_dungeons(player.get("dungeons")))
def print_armor_and_equipment(player):
    #armour and equipment
    #armour
    print()
    print("Armour:")
    armor_data = player["inventory"]["inv_armor"]["data"]
    armor = decode_inventory_data(armor_data)
    armor_items = armor[""]["i"]
    armor_slots = [
        "Helmet",
        "Chestplate",
        "Leggings",
        "Boots"
    ]
    for index, item in enumerate(reversed(armor_items)):
        raw_item_name = item["tag"]["display"]["Name"]
        item_name = remove_minecraft_color_codes(raw_item_name)
        rarity = get_item_rarity(raw_item_name)
        print(f"{armor_slots[index]}: {item_name} ({rarity})")
    #equipments
    print()
    print("Equipment:")
    equipment_data = player["inventory"]["equipment_contents"]["data"]
    equipment = decode_inventory_data(equipment_data)
    equipment_items = equipment[""]["i"]
    equipment_slots = [
        "Necklace",
        "Cloak",
        "Belt",
        "Gloves"
    ]
    for index, item in enumerate(equipment_items):
        raw_item_name = item["tag"]["display"]["Name"]
        item_name = remove_minecraft_color_codes(raw_item_name)
        rarity = get_item_rarity(raw_item_name)
        print(f"{equipment_slots[index]}: {item_name} ({rarity})")
def print_active_pet(player):
    #active pet
    active_pet = None
    for pet in player["pets_data"]["pets"]:
        if pet["active"]:
            active_pet = pet
            break
    print()
    if active_pet:
        pet_name = active_pet["type"].replace("_", " ").title()
        pet_rarity = active_pet["tier"].title()
        print(f"Active Pet: {pet_rarity} {pet_name}")
    else:
        print("Active Pet: None")
def main():
    print("MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM")
    print("        Skyblock Stats        ")
    print("MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM")
    print()
    username = input("Enter Minecraft Username: ")
    print(f"Searching for {username}...")
    with httpx.Client(
        http2=False,
        timeout=30
    ) as client:
        uuid = get_minecraft_uuid(client, username)
        if uuid is None:
            return
        hypixel_data = get_hypixel_data(client, uuid)
        if hypixel_data is None:
            return
        with open("hypixel_data.json", "w") as file:
            json.dump(hypixel_data, file, indent=4)
        skills_data = get_skills_data(client)
        if skills_data is None:
            return
        selected_profile = get_selected_profile(hypixel_data)
        if selected_profile is None:
            print("No selected SkyBlock profile found.")
            return
        player = print_profile_info(selected_profile, uuid)
        print_skills(player, skills_data)
        print_dungeons_info(player)
        print_armor_and_equipment(player)
        print_active_pet(player)
if __name__ == "__main__":
    main()
