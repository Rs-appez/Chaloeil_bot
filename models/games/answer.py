class Answer():
      
    def __init__(self, json) -> None:

        self.answer_text = json["answer_text"]
        self.is_correct = json["is_correct"]
        self.emoji = json["emoticon"]
