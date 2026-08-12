def format_money(amount):

    if amount >= 1_000_000_000:
        return f"{amount / 1_000_000_000:.1f}B"

    elif amount >= 1_000_000:
        return f"{amount / 1_000_000:.1f}M"

    elif amount >= 1_000:
        return f"{amount / 1_000:.1f}K"

    return f"{amount:.0f}"
def format_level(experience):

    level = experience // 100
    progress = experience % 100

    return f"{level}.{progress:02d}"