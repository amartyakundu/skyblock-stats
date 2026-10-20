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
from dungeons import format_dungeons, get_dungeons_data


class InvalidUsernameError(Exception):
    pass


def get_minecraft_uuid(client, username):
    #mojang api
    username = username.strip()
    if not username:
        raise InvalidUsernameError("Please enter a Minecraft username.")

    mojang_url = f"https://api.minecraftservices.com/minecraft/profile/lookup/name/{username}"
    mojang_response = client.get(mojang_url)

    if mojang_response.status_code == 200:
        mojang_data = mojang_response.json()
        return mojang_data["id"]

    elif mojang_response.status_code in (400, 404):
        raise InvalidUsernameError("Invalid username or player not found.")

    raise RuntimeError(f"Mojang API Error: {mojang_response.status_code}")


def get_hypixel_data(client, uuid):
    # hypixel API
    hypixel_url = f"https://api.hypixel.net/v2/skyblock/profiles?uuid={uuid}"
    headers = {
        "API-Key": API_KEY
    }
    hypixel_response = client.get(hypixel_url, headers=headers)

    if hypixel_response.status_code != 200:
        raise RuntimeError(f"Hypixel API Error: {hypixel_response.status_code}")

    return hypixel_response.json()


def get_skills_resource(client):
    #skills api
    skills_url = "https://api.hypixel.net/v2/resources/skyblock/skills"
    skills_response = client.get(skills_url)

    if skills_response.status_code != 200:
        raise RuntimeError(f"Skills API Error: {skills_response.status_code}")

    return skills_response.json().get("skills") or {}


def load_skyblock_data(username):
    #load profile data
    with httpx.Client(
        http2=False,
        timeout=30
    ) as client:
        uuid = get_minecraft_uuid(client, username)
        hypixel_data = get_hypixel_data(client, uuid)
        skills_data = get_skills_resource(client)

    return {
        "uuid": uuid,
        "hypixel_data": hypixel_data,
        "skills_resource": skills_data,
        "profiles": hypixel_data.get("profiles") or [],
    }


def get_selected_profile(profiles):
    #active profile finder
    for profile in profiles or []:
        if profile.get("selected"):
            return profile

    return None


def get_profile_overview(selected_profile, player):
    #profile info
    leveling = player.get("leveling") or {}
    currencies = player.get("currencies") or {}
    profile_data = player.get("profile") or {}
    fairy_souls = player.get("fairy_soul") or {}

    return {
        "profile_name": selected_profile.get("cute_name") or "Unknown",
        "profile_type": selected_profile.get("game_mode") or "Normal",
        "level_experience": leveling.get("experience"),
        "purse": currencies.get("coin_purse"),
        "bank": profile_data.get("bank_account"),
        "fairy_souls": fairy_souls.get("total_collected"),
    }


def get_player_skills(player, skills_resource):
    #skills info
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

    player_data = player.get("player_data") or {}
    player_skill_xp = player_data.get("experience") or {}
    skills = []

    for skill_name, xp_key in skill_names:
        skill_xp = player_skill_xp.get(xp_key, 0)
        skill_info = skills_resource.get(skill_name)
        if not skill_info or not skill_info.get("levels"):
            continue

        skill_level, current_xp, xp_needed, overflow_xp = get_skill_progress(
            skill_xp,
            skill_info["levels"]
        )

        skills.append({
            "name": skill_info["name"],
            "level": skill_level,
            "current_xp": current_xp,
            "xp_needed": xp_needed,
            "overflow_xp": overflow_xp,
            "max_level": skill_info["maxLevel"],
        })

    return skills


def get_armor_and_equipment(player):
    #armour and equipment
    inventory = player.get("inventory") or {}

    armor_data = (inventory.get("inv_armor") or {}).get("data")
    armor_items = []
    if armor_data:
        armor = decode_inventory_data(armor_data)
        armor_items = (armor.get("") or {}).get("i") or []

    armor_slots = [
        "Helmet",
        "Chestplate",
        "Leggings",
        "Boots"
    ]

    armor_display_data = []
    armor_items = list(reversed(armor_items))
    for index, slot in enumerate(armor_slots):
        item = armor_items[index] if index < len(armor_items) else None
        armor_display_data.append(get_item_display_data(item, slot))

    #equipments
    equipment_data = (inventory.get("equipment_contents") or {}).get("data")
    equipment_items = []
    if equipment_data:
        equipment = decode_inventory_data(equipment_data)
        equipment_items = (equipment.get("") or {}).get("i") or []

    equipment_slots = [
        "Necklace",
        "Cloak",
        "Belt",
        "Gloves"
    ]

    equipment_display_data = []
    for index, slot in enumerate(equipment_slots):
        item = equipment_items[index] if index < len(equipment_items) else None
        equipment_display_data.append(get_item_display_data(item, slot))

    return {
        "armor": armor_display_data,
        "equipment": equipment_display_data,
    }


def get_item_display_data(item, slot):
    #item display info
    if not item:
        return {"slot": slot, "name": "Empty", "rarity": None}

    item_tag = item.get("tag") or {}
    display_data = item_tag.get("display") or {}
    raw_item_name = display_data.get("Name")

    if not raw_item_name:
        return {"slot": slot, "name": "Empty", "rarity": None}

    return {
        "slot": slot,
        "name": remove_minecraft_color_codes(raw_item_name),
        "rarity": get_item_rarity(raw_item_name),
    }


def get_active_pet(player):
    #active pet
    pets_data = player.get("pets_data") or {}
    for pet in pets_data.get("pets") or []:
        if pet.get("active"):
            return {
                "name": (pet.get("type") or "Unknown").replace("_", " ").title(),
                "rarity": (pet.get("tier") or "Unknown").title(),
            }

    return None


def get_profile_data(profile, uuid, skills_resource):
    #profile data
    members = profile.get("members") or {}
    player = members.get(uuid) or {}

    return {
        "overview": get_profile_overview(profile, player),
        "skills": get_player_skills(player, skills_resource),
        "dungeons": get_dungeons_data(player.get("dungeons")),
        "armor_and_equipment": get_armor_and_equipment(player),
        "active_pet": get_active_pet(player),
    }


def print_profile_overview(overview):
    #profile output
    print(f"Selected Profile: {overview['profile_name']}")
    print(f"Profile Type: {overview['profile_type']}")

    level = overview["level_experience"]
    purse = overview["purse"]
    bank = overview["bank"]
    fairy_souls = overview["fairy_souls"]

    print(f"SkyBlock Level: {format_level(level) if level is not None else 'Unavailable'}")
    print(f"Purse: {format_money(purse) if purse is not None else 'Unavailable'}")
    print(f"Bank: {format_money(bank) if bank is not None else 'Unavailable'}")
    print(f"Total Fairy Souls Collected: {fairy_souls if fairy_souls is not None else 'Unavailable'}")


def print_skills(skills):
    #skills output
    print()
    print("Skills:")

    for skill in skills:
        if skill["level"] == skill["max_level"]:
            print(
                f"{skill['name']} {skill['level']} | "
                f"Overflow: {skill['overflow_xp']:,.0f} XP"
            )
        else:
            print(
                f"{skill['name']} {skill['level']} | "
                f"{skill['current_xp']:,.0f}/{skill['xp_needed']:,.0f} XP"
            )


def print_dungeons_info(dungeons):
    #dungeons info
    print()
    print(format_dungeons(dungeons))


def print_armor_and_equipment(armor_and_equipment):
    #armour and equipment
    print()
    print("Armour:")
    for item in armor_and_equipment["armor"]:
        if item["rarity"]:
            print(f"{item['slot']}: {item['name']} ({item['rarity']})")
        else:
            print(f"{item['slot']}: {item['name']}")

    #equipments
    print()
    print("Equipment:")
    for item in armor_and_equipment["equipment"]:
        if item["rarity"]:
            print(f"{item['slot']}: {item['name']} ({item['rarity']})")
        else:
            print(f"{item['slot']}: {item['name']}")


def print_active_pet(active_pet):
    #active pet output
    print()
    if active_pet:
        print(f"Active Pet: {active_pet['rarity']} {active_pet['name']}")
    else:
        print("Active Pet: None")


def print_profile_data(profile_data):
    #CLI output
    print_profile_overview(profile_data["overview"])
    print_skills(profile_data["skills"])
    print_dungeons_info(profile_data["dungeons"])
    print_armor_and_equipment(profile_data["armor_and_equipment"])
    print_active_pet(profile_data["active_pet"])


def main():
    print("MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM")
    print("        Skyblock Stats        ")
    print("MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM")
    print()

    while True:
        username = input("Enter Minecraft Username: ")
        print(f"Searching for {username}...")

        try:
            skyblock_data = load_skyblock_data(username)
            selected_profile = get_selected_profile(skyblock_data["profiles"])
            if selected_profile is None:
                print("No selected SkyBlock profile found.")
                print("Please try another username.")
                continue
            break
        except InvalidUsernameError as error:
            print(error)
            print("Please try again.")
        except (RuntimeError, httpx.RequestError, json.JSONDecodeError) as error:
            print(error)
            return

    with open("hypixel_data.json", "w") as file:
        json.dump(skyblock_data["hypixel_data"], file, indent=4)

    profile_data = get_profile_data(
        selected_profile,
        skyblock_data["uuid"],
        skyblock_data["skills_resource"],
    )
    print_profile_data(profile_data)


if __name__ == "__main__":
    main()
