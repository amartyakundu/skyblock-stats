"""Format the dungeon data from a SkyBlock profile member."""

from itertools import accumulate

from formatting import get_skill_progress


# XP per level (1-50), shared by Catacombs and dungeon classes.
# Source: https://github.com/NotEnoughUpdates/NotEnoughUpdates-REPO/blob/master/constants/leveling.json
DUNGEON_XP = (
    50, 75, 110, 160, 230, 330, 470, 670, 950, 1340,
    1890, 2665, 3760, 5260, 7380, 10300, 14400, 20000, 27600, 38000,
    52500, 71500, 97000, 132000, 180000, 243000, 328000, 445000, 600000, 800000,
    1065000, 1410000, 1900000, 2500000, 3300000, 4300000, 5600000,
    7200000, 9200000, 12000000, 15000000, 19000000, 24000000,
    30000000, 38000000, 48000000, 60000000, 75000000, 93000000, 116250000,
)
DUNGEON_LEVELS = [
    {"level": level, "totalExpRequired": total}
    for level, total in enumerate(accumulate(DUNGEON_XP), start=1)
]


def format_dungeon_level(name, experience):
    level, current_xp, xp_needed, overflow = get_skill_progress(
        experience or 0, DUNGEON_LEVELS
    )
    if level == 50:
        return f"{name} {level} | Overflow: {overflow:,.0f} XP"
    return f"{name} {level} | {current_xp:,.0f}/{xp_needed:,.0f} XP"


def format_dungeons(dungeons):
    lines = ["Dungeons:"]
    if not dungeons:
        return "\n".join(lines + ["No dungeon data available."])

    dungeon_types = dungeons.get("dungeon_types") or {}
    catacombs = dungeon_types.get("catacombs") or {}
    lines.append(format_dungeon_level("Catacombs", catacombs.get("experience", 0)))
    selected_class = dungeons.get("selected_dungeon_class")
    lines.append(f"Selected Class: {selected_class.title() if selected_class else 'None'}")
    secrets = dungeons.get("secrets")
    lines.append(f"Secrets Found: {secrets:,.0f}" if secrets is not None else "Secrets Found: Unavailable")

    classes = dungeons.get("player_classes") or {}
    for name in ("healer", "mage", "berserk", "archer", "tank"):
        class_data = classes.get(name) or {}
        lines.append(format_dungeon_level(name.title(), class_data.get("experience", 0)))

    for key, label, prefix, floors in (
        ("catacombs", "Catacombs Completions", "F", range(8)),
        ("master_catacombs", "Master Mode Completions", "M", range(1, 8)),
    ):
        dungeon = dungeon_types.get(key) or {}
        completions = dungeon.get("tier_completions") or {}
        counts = []
        for floor in floors:
            name = "Entrance" if floor == 0 else f"{prefix}{floor}"
            counts.append(f"{name}: {completions.get(str(floor), 0):,.0f}")
        lines.append(f"{label}: " + " | ".join(counts))

    return "\n".join(lines)
