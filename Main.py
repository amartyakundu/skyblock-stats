import httpx
from config import API_KEY
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

mojang_response = client.get(Mojang_url)

print(f"Status Code: {mojang_response.status_code}")
#GET UIID 
if mojang_response.status_code == 200:
    mojang_data = mojang_response.json()

    uuid = mojang_data["id"]

    print(f"UUID: {uuid}")

    # Hypixel API
    hypixel_url = f"https://api.hypixel.net/v2/skyblock/profiles?uuid={uuid}"

    headers = {
        "API-Key": API_KEY
    }

    hypixel_response = client.get(hypixel_url, headers=headers)

    print(f"Hypixel Status Code: {hypixel_response.status_code}")

    hypixel_data = hypixel_response.json()

    print(hypixel_data.keys())

else:
    print("Player not found.")