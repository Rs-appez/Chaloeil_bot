import random


class Dice:
    def __init__(self, number=1, sides=6):
        self.sides = sides
        self.number = number

        self.emojis = {
            1: "<:dice_1:1386378550956920902>",
            2: "<:dice_2:1386378565410623498>",
            3: "<:dice_3:1386378574436499456>",
            4: "<:dice_4:1386378583210983536>",
            5: "<:dice_5:1386378592581320775>",
            6: "<:dice_6:1386378600776859870>",
        }

        self.result = None

    def roll(self):
        self.result = [random.randint(1, self.sides)
                       for _ in range(self.number)]

    def verbal_roll(self, user="Tu"):
        if not self.result:
            self.roll()
        return f"{user} a obtenu : {sum(self.result)}"

    def image_roll(self):
        if not self.result:
            self.roll()
        return " ".join(
            [str(self.emojis[d]) if 1 <= d <= 6 else str(d)
             for d in self.result]
        )
