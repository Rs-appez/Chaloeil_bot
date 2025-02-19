from models.games.answer import Answer
import config
import requests
import random

from nextcord import Member, Interaction
from views.games.answerView import AnswerView


class Question:
    api_url = config.BACKEND_URL + "question/questions/"

    def __init__(self, json) -> None:
        self.id = json["id"]
        self.question = json["question_text"]
        self.answers = [Answer(a) for a in json["answers"]]
        self.level = json["level"]
        self.cat = json["categories"]
        self.image_url = json["image_url"]
        self.shuffle_answers = json["shuffle_answers"]

    @staticmethod
    def get_question(number, level=None, cat=None, id_range=None):
        req = requests.get(
            Question.api_url + "random_question",
            params={
                "level": level,
                "category": cat,
                "number": number,
                "id_range": id_range,
            },
            headers={"Authorization": config.BACKEND_TOKEN},
        )

        if req.status_code == 200:
            if number == 1:
                return [Question(req.json()[0])]
            else:
                return [Question(q) for q in req.json()]
        else:
            return None

    def get_answers(self):
        answers = self.answers
        if self.shuffle_answers:
            random.shuffle(answers)

        return answers

    def get_good_answers(self):
        return [a.answer_text for a in self.answers if a.is_correct]

    def check_answer(self, answer):
        return [
            a for a in self.answers if a.is_correct and a.answer_text == answer
        ] != []

    async def ask_standalone(self, player: Member, interaction: Interaction):
        question_msg = f"‎ ‎\n**{self.question}**\n‎ ‎"
        await interaction.response.send_message(
            content=question_msg,
            view=AnswerView(question=self, player=player),
        )
