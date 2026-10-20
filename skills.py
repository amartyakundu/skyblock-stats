"""Get and calculate skill data for a SkyBlock profile member."""

from formatting import get_skill_progress


def get_skills_resource(client):
    #skills api
    skills_url = "https://api.hypixel.net/v2/resources/skyblock/skills"
    skills_response = client.get(skills_url)

    if skills_response.status_code != 200:
        raise RuntimeError(f"Skills API Error: {skills_response.status_code}")

    return skills_response.json().get("skills") or {}


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
