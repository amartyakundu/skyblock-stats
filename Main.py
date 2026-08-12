import httpx
from formatting import format_money, format_level
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
# GET UUID
if mojang_response.status_code == 200:

    mojang_data = mojang_response.json()

    uuid = mojang_data["id"]

    # Hypixel API
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

    for profile in hypixel_data["profiles"]:

        if profile["selected"]:
            selected_profile = profile
            break
    
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
elif mojang_response.status_code == 404:
    print("Player not found.")
else:
    print(f"Mojang API Error: {mojang_response.status_code}")