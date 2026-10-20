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


def get_dungeon_level(name, experience):
    level, current_xp, xp_needed, overflow = get_skill_progress(
        experience or 0, DUNGEON_LEVELS
    )
    return {
        "name": name,
        "level": level,
        "current_xp": current_xp,
        "xp_needed": xp_needed,
        "overflow_xp": overflow,
        "max_level": DUNGEON_LEVELS[-1]["level"],
    }


def get_dungeon_floors(dungeon_type, prefix, floor_numbers):
    tier_completions = dungeon_type.get("tier_completions") or {}
    best_runs = dungeon_type.get("best_runs") or {}
    floors = []

    for floor in floor_numbers:
        floor_key = str(floor)
        floor_name = "Entrance" if floor == 0 else f"{prefix}{floor}"
        floor_stats = {}

        for stat_name, stat_values in dungeon_type.items():
            if stat_name in ("tier_completions", "best_runs"):
                continue
            if isinstance(stat_values, dict) and floor_key in stat_values:
                floor_stats[stat_name] = stat_values[floor_key]

        floors.append({
            "name": floor_name,
            "floor": floor,
            "completions": tier_completions.get(floor_key, 0),
            "stats": floor_stats,
            "best_runs": best_runs.get(floor_key) or [],
        })

    return floors


def get_dungeons_data(dungeons):
    #dungeons info
    if not dungeons:
        return None

    dungeon_types = dungeons.get("dungeon_types") or {}
    catacombs = dungeon_types.get("catacombs") or {}
    classes = dungeons.get("player_classes") or {}
    master_catacombs = dungeon_types.get("master_catacombs") or {}

    class_levels = []
    for name in ("healer", "mage", "berserk", "archer", "tank"):
        class_data = classes.get(name) or {}
        class_levels.append(
            get_dungeon_level(name.title(), class_data.get("experience", 0))
        )

    return {
        "catacombs": get_dungeon_level(
            "Catacombs", catacombs.get("experience", 0)
        ),
        "selected_class": dungeons.get("selected_dungeon_class"),
        "secrets": dungeons.get("secrets"),
        "class_levels": class_levels,
        "highest_floor_normal": catacombs.get("highest_tier_completed"),
        "highest_floor_master": master_catacombs.get("highest_tier_completed"),
        "normal_floors": get_dungeon_floors(
            catacombs, "F", range(8)
        ),
        "master_floors": get_dungeon_floors(
            master_catacombs, "M", range(1, 8)
        ),
    }


def format_dungeon_level(level_data):
    name = level_data["name"]
    level = level_data["level"]

    if level == level_data["max_level"]:
        return f"{name} {level} | Overflow: {level_data['overflow_xp']:,.0f} XP"

    return (
        f"{name} {level} | "
        f"{level_data['current_xp']:,.0f}/{level_data['xp_needed']:,.0f} XP"
    )


def format_dungeons(dungeon_data):
    #CLI dungeon output
    lines = ["Dungeons:"]
    if not dungeon_data:
        return "\n".join(lines + ["No dungeon data available."])

    lines.append(format_dungeon_level(dungeon_data["catacombs"]))
    selected_class = dungeon_data.get("selected_class")
    lines.append(f"Selected Class: {selected_class.title() if selected_class else 'None'}")

    secrets = dungeon_data.get("secrets")
    lines.append(f"Secrets Found: {secrets:,.0f}" if secrets is not None else "Secrets Found: Unavailable")

    for class_level in dungeon_data["class_levels"]:
        lines.append(format_dungeon_level(class_level))

    for label, key in (
        ("Catacombs Completions", "normal_floors"),
        ("Master Mode Completions", "master_floors"),
    ):
        counts = [
            f"{floor['name']}: {floor['completions']:,.0f}"
            for floor in dungeon_data[key]
        ]
        lines.append(f"{label}: " + " | ".join(counts))

    return "\n".join(lines)

