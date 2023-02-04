class Quiz:
    total_score = None
    questions = []
    updated_date = None
    created_by = None
    submitted_date = None
    submitted_by = None

    def __init__(self):
        self.total_score = Score()


class Question:
    question_text = ''
    response_options = []
    active = True


class ResponseOption:
    response_text = ''
    response_score = None
    response_selected = False


class Score:
    gryffindor = 0
    ravenclaw = 0
    hufflepuff = 0
    slytherin = 0
