class Answer():
      
    def __init__(self, good_answer, bad_answers) -> None:
        self.bad_answers = bad_answers
        self.good_answer = good_answer

    
    def show_answers(self):

        return self.bad_answers.append(self.good_answer).shuffle()