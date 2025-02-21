from bson import ObjectId

from ProjetFinalnosql.model.AnswerModel import AnswerModel




class QuestionModel:
    def __init__(self,id, intitule, type, reponses=None):
        self.id = ObjectId(id)
        self.intitule = intitule
        self.type = type
        if type == "multiple":
            self.reponses = reponses
        else:
            self.reponses = None

    def __str__(self):
        return "QuestionModel(id={},intitule={},type={},reponses={})".format(self.id,self.intitule,self.type,self.reponses)