from models.games.answer import Answer
import config
import requests

class Question():

    api_url = config.BACKEND_URL + "question/questions/"

    def __init__(self, json) -> None:
        self.question = json["question_text"]
        self.answer = Answer(json["answers"])
        self.level = json["level"]
        self.cat = json["categories"]

    @staticmethod
    def get_question(level = None, cat = None):

        req = requests.get(Question.api_url + "random_question",params={"level":level,"cat":cat},headers={"Authorization":config.BACKEND_TOKEN})

        if req.status_code == 200:
            return Question(req.json())
        else :
            raise Exception("Error when getting question")
    def get_answers(self):

        return self.answer.show_answers()
        
    def get_good_answers(self) :

        return self.answer.good_answers
    
    def check_answer(self,answer):

        return self.answer.check_answer(answer)
