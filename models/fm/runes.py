class Rune:
    image_url = "https://media.discordapp.net/attachments/1370085525708341258/1434334943391125524/radin_tableau_transcendance_BLANC.png"
    stats = {
        "fo": {"ta": 61, "pata": 41, "rata": 21},
        "ine": {"ta": 61, "pata": 41, "rata": 21},
        "age": {"ta": 61, "pata": 41, "rata": 21},
        "cha": {"ta": 61, "pata": 41, "rata": 21},
        "vi": {"ta": 301, "pata": 204, "rata": 105},
        "ini": {"ta": 610, "pata": 410, "rata": 210},
        "pui": {"ta": 30, "pata": 20, "rata": 10},
        "ré per": {"ta": 3},
        "ré pou": {"ta": 20, "pata": 10},
        "ré cri": {"ta": 17, "pata": 10},
        "ret": {"ta": 8, "pata": 5, "rata": 3},
        "pod": {"ta": 250, "pata": 150, "rata": 90},
        "tac/fui": {"ta": 15, "pata": 10, "rata": 5},
        "do": {"ta": 12, "pata": 8, "rata": 4},
        "do cri": {"ta": 8, "pata": 4},
        "so": {"ta": 6, "pata": 4, "rata": 2},
        "cri": {"ta": 6, "pata": 2},
        "do per di": {"ta": 3},
        "do per mé": {"ta": 3},
        "do per ar": {"ta": 3},
        "do per so": {"ta": 3},
    }

    @staticmethod
    def get_rune_info(stat: str) -> str:
        if stat in Rune.stats:
            rune_info = Rune.stats[stat]
            info_lines = [
                f"### Maximum stats pour les runes **{stat}** de transcendence:"
            ]
            for rune_type, value in rune_info.items():
                info_lines.append(f"* {rune_type:<4} : {value}")
            return "\n".join(info_lines)
        else:
            return f"No transcendence information available for {stat}."

    @staticmethod
    def get_all_rune_info() -> str:
        info_lines = []
        for stat, rune_info in Rune.stats.items():
            info_lines.append(Rune.get_rune_info(stat))
            info_lines.append("")
        return "\n".join(info_lines)
