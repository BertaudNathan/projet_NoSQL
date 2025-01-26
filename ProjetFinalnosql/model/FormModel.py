from ProjetFinalnosql.model.AnswerModel import AnswerModel


class FormModel:
    def __init__(self, objectId, DictQuestion, title, description, password):
        self.objectId = objectId
        self.title = title
        self.description = description
        self.password = password
        self.DictQuestion = DictQuestion

    def canEdit(self, password):
        return self.password == password

    def AnswerForm(self, DictAnswer):
        return AnswerModel(self.objectId, DictAnswer)