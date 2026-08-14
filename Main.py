import httpx
from formatting import format_money, format_level, get_skill_progress
from config import API_KEY
import json

print("==============================")
print("        Skyblock Stats        ")
print("==============================")
print()

username = input("Enter Minecraft Username: ")
print(f"Searching for {username}...")

mojang_url = f"https://api.minecraftservices.com/minecraft/profile/lookup/name/{username}"

client = httpx.Client(
    http2=False,
    timeout=30
)

mojang_response = client.get(mojang_url)

#mojang api
if mojang_response.status_code == 200:
    mojang_data = mojang_response.json()

    uuid = mojang_data["id"]

    # hypixel API
    hypixel_url = f"https://api.hypixel.net/v2/skyblock/profiles?uuid={uuid}"

    headers = {
        "API-Key": API_KEY
    }

    hypixel_response = client.get(hypixel_url, headers=headers)

    if hypixel_response.status_code != 200:
        print(f"Hypixel API Error: {hypixel_response.status_code}")
        exit()

    hypixel_data = hypixel_response.json()

    with open("hypixel_data.json", "w") as file:
        json.dump(hypixel_data, file, indent=4)

    #skills api
    skills_url = "https://api.hypixel.net/v2/resources/skyblock/skills"

    skills_response = client.get(skills_url)

    if skills_response.status_code != 200:
        print(f"Skills API Error: {skills_response.status_code}")
        exit()

    skills_data = skills_response.json()["skills"]
    #active profile finder
    for profile in hypixel_data["profiles"]:

        if profile["selected"]:
            selected_profile = profile
            break
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
    #skills output
            print(
                f"{display_name} {skill_level} | "
                f"Overflow: {overflow_xp:,.0f} XP"
            )
        else:
            print(
                f"{display_name} {skill_level} | "
                f"{current_xp:,.0f}/{xp_needed:,.0f} XP"
            )

elif mojang_response.status_code == 404:
    print("Player not found.")

else:
    print(f"Mojang API Error: {mojang_response.status_code}")