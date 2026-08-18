from config import DEBUG


class RaidInfo:
    questions = {
        "belladone": {
            "content": "Raid Sanctuaire des Jardins éternels\n__Durée : 2h__",
            "question": "Quelles sont vos disponibilités?",
        },
        "gigalodon": {
            "content": "Raid Gouffre du Gigalodon\n__Durée : un peu plus que 1h__",
            "question": "Quelles sont vos disponibilités?",
        },
    }
    options = (
        [
            "Samedi 17 h",
            "Samedi 18 h",
            "Samedi 20h30",
            "Samedi 21h30",
            "Dimanche 16h",
            "Dimanche 17h",
            "Dimanche 18h",
            "Dimanche 20h30",
        ],
    )

    @staticmethod
    def get_raid_poll_payload(raid_id):
        answers = [{"poll_media": {"text": option}} for option in RaidInfo.options[0]]
        answers.append(
            {
                "poll_media": {
                    "text": "Tout me va !",
                    "emoji": {"id": 1539397731095941241}
                    if not DEBUG
                    else {"name": "✅"},
                }
            }
        )
        return {
            "content": "# " + RaidInfo.questions[raid_id]["content"],
            "poll": {
                "question": {"text": RaidInfo.questions[raid_id]["question"]},
                "answers": answers,
                "duration": 24 * 3,
                "allow_multiselect": True,
                "layout_type": 1,
            },
        }
