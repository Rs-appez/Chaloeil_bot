import random
class Answer():
      
    def __init__(self, json) -> None:

        self.bad_answers = [a["answer_text"] for a in json if not a["is_correct"]]
        self.good_answers = [a["answer_text"] for a in json if a["is_correct"]]

    
    def show_answers(self):
        answers = []
        answers.extend(self.bad_answers)
        answers.extend(self.good_answers)
        random.shuffle(answers)
        return answers
    
    def check_answer(self,answer):

        return  answer in self.good_answers