import random
class Answer():
      
    def __init__(self, good_answer, bad_answers) -> None:
        self.bad_answers = bad_answers
        self.good_answer = good_answer

    
    def show_answers(self):
        
        answer = self.bad_answers.copy()
        answer.append(self.good_answer)
        random.shuffle(answer)
        return answer