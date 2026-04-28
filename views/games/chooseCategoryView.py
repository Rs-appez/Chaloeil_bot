from nextcord import ButtonStyle, SelectOption
from nextcord.ui import Select, View, button


class ChooseCategoryView(View):
    choices = {
        "Une question sur les maps": "map",
        "Une question sur les succès": "succes",
        "Une question sur les archimonstres": "archimonstre",
        "Une question sur les items": "item",
        "Une question sur les sorts": "sort",
        "Une question sur les classes": "classe",
        "Une question sur la géographie": "géographie",
        "Une question sur les quêtes": "quete",
        "Une question de la catégorie divers s'il vous plaît": "divers",
    }

    def __init__(self, game) -> None:
        super().__init__()

        self.game = game
        self.message = None
        select = Select(
            placeholder="Choisis une catégorie",
            options=[
                SelectOption(label=label, value=value)
                for label, value in self.choices.items()
            ],
        )
        select.callback = self.select_callback
        self.add_item(select)

    async def select_callback(self, interaction):
        selected = interaction.data["values"][0]
        if not self.message:
            self.message = await interaction.response.send_message(
                content=f"Tu as choisi la catégorie {selected}. Es-tu prêt ???",
                view=LaunchCategoryView(self.game, selected),
            )
        else:
            await self.message.edit(
                content=f"Tu as choisi la catégorie {selected}. Es-tu prêt ???",
                view=LaunchCategoryView(self.game, selected),
            )


class LaunchCategoryView(View):
    def __init__(self, game, choice) -> None:
        super().__init__(timeout=None)

        self.game = game
        self.choice = choice

    @button(label="Je suis prêt !", style=ButtonStyle.green, emoji="🫡")
    async def statement(self, button, interaction):
        button.disabled = True
        await interaction.response.edit_message(view=self)
        await self.game.load_final_question(self.choice)
