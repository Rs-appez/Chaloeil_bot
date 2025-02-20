import random


class Dice:
    def __init__(self, bot, number=1, sides=6):
        self.sides = sides
        self.number = number

        self.emojis = {
            1: bot.ch_emojis["dice_1"] if "dice_1" in bot.ch_emojis else "1",
            2: bot.ch_emojis["dice_2"] if "dice_2" in bot.ch_emojis else "2",
            3: bot.ch_emojis["dice_3"] if "dice_3" in bot.ch_emojis else "3",
            4: bot.ch_emojis["dice_4"] if "dice_4" in bot.ch_emojis else "4",
            5: bot.ch_emojis["dice_5"] if "dice_5" in bot.ch_emojis else "5",
            6: bot.ch_emojis["dice_6"] if "dice_6" in bot.ch_emojis else "6",
        }

        self.result = None

    def roll(self):
        self.result = [random.randint(1, self.sides)
                       for _ in range(self.number)]

    def verbal_roll(self, user="Tu"):
        if not self.result:
            self.roll()
        return f"{user} as obtenu : {sum(self.result)}"

    def image_roll(self):
        if not self.result:
            self.roll()
        message = ""
        for d in self.result:
            message += self.emojis[d] + " "
        return message
