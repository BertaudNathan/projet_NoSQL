from ProjetFinalnosql.model.AnswerModel import AnswerModel


class FormModel:
    def __init__(self, Questions, title, description, password):
        self.title = title
        self.description = description
        self.password = password
        self.Questions = Questions

    def canEdit(self, password):
        return self.password == password

    def __str__(self):
        q = [q.__str__() for q in self.Questions]
        return "FormModel(title={},description={},password={},Questions={})".format(self.title,self.description,self.password,q)