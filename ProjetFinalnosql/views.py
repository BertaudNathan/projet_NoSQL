from bson import ObjectId
from pymongo import MongoClient
from django.http import HttpResponse
from django.shortcuts import redirect, render
from ProjetFinalnosql.model.FormModel import FormModel
from ProjetFinalnosql.model.QuestionModel import QuestionModel



def home(request):
    db = MongoClient().get_database("base_formulaires")
    collection = db["Formulaires"]
    forms = collection.find({}).to_list();
    for i in forms:
        i["id"] = str(i["_id"])
    if 'success' in request.session:
        success = request.session['success']
        del request.session['success']
        return render(request, 'home.html', {"page_title": "Accueil", "success": success, "forms": forms})
    elif 'error' in request.session:
        error = request.session['error']
        del request.session['error']
        return render(request, 'home.html', {"page_title": "Accueil", "error": error, "forms": forms})
    elif 'info' in request.session:
        info = request.session['info']
        del request.session['info']
        return render(request, 'home.html', {"page_title": "Accueil", "info": info, "forms": forms})
    return render(request, 'home.html', {"page_title": "Accueil", "forms": forms})


def form(request,uuid):
    db = MongoClient().get_database("base_formulaires")
    collection = db["Formulaires"]
    dictForm = collection.find_one(ObjectId(uuid))
    if dictForm is None:
        return render(request, '404.html', {"page_title": "Cette page n'existe pas."}, status=404)
    dictForm = dict(dictForm)
    Questions = []
    for question in dictForm["Questions"]:
        Questions.append(QuestionModel(question["_id"],question["intitule"],question["type"],question["reponses"] if question["type"] == "multiple" else None))
    form = FormModel(uuid, Questions,dictForm["nom"],dictForm["description"],dictForm["password"])
    return render(request, 'form.html', {"page_title": "Repondre a un formulaire", "form": form, "uuid": uuid})

def create_form(request):
    if request.method == 'POST':
        form_data = request.POST
        dictValidate={}
        Questions = []
        dictForm = {
            key: form_data.getlist(key) if len(form_data.getlist(key)) > 1 else form_data.get(key)
            for key in form_data.keys()
        }
        for key, value in dictForm.items():
            if key.startswith(('question')):#', 'reponse', 'form_title', 'form_description','form_password')):
                if key.startswith('questionMultiple'):
                    Questions.append({"_id": ObjectId() ,"intitule":value.strip(), "type":"multiple", "reponses":dictForm["reponse"+key[len("questionMultiple"):]]})
                else:
                    Questions.append({"_id": ObjectId() ,"intitule":value.strip(), "type":"unique"})

        try:
            db = MongoClient().get_database("base_formulaires")
            collection = db["Formulaires"]
            collection.insert_one({"nom":dictForm["form_title"],"description":dictForm["form_description"],"password":dictForm["form_password"],"Questions":Questions})
            request.session['success'] = 'Votre formulaire a été créé.'
            return redirect('/home')
        except Exception as e:
            print("Erreur lors de l'insertion dans MongoDB:", e)
            return HttpResponse("Erreur lors de l'insertion des données.", status=500)




    elif request.method == 'GET':
        return render(request, 'create_form.html', {"page_title": "Créer un formulaire"})


def form_as_admin(request,uuid):
    if request.method == 'POST':
        form_data = request.POST
        db = MongoClient().get_database("base_formulaires")
        collection = db["Formulaires"]
        f = collection.find_one(ObjectId(uuid))
        dictForm = dict(f)
        Questions = []
        for question in dictForm["Questions"]:
            Questions.append(QuestionModel(question["_id"], question["intitule"], question["type"],
                                           question["reponses"] if question["type"] == "multiple" else None))
        form = FormModel(uuid,Questions, dictForm["nom"], dictForm["description"], dictForm["password"].strip())
        if form_data["password"].strip() == form.password:
            return render(request, 'update_form.html', {"page_title": "Mettre à jour un formulaire", "form": form})
        else:
            request.session['error'] = 'Le mot de passe est invalide.'
            return redirect('/home')
    return render(request, '404.html', {"page_title": "Cette page n'existe pas."}, status=404)


def answer_form(request,uuid):
    if request.method == 'POST':
        if uuid is None:
            return render(request, '404.html', {"page_title": "This page does not exist."}, status=404)
        form_data = request.POST
        dictValidate={}
        reponses = []
        db = MongoClient().get_database("base_formulaires")
        collection = db["Reponses"]
        dictForm = {
            key: form_data.getlist(key) if len(form_data.getlist(key)) > 1 else form_data.get(key)
            for key in form_data.keys()
        }
        dictForm.pop("csrfmiddlewaretoken")

        for key, value in dictForm.items():

            if db["Formulaires"].find_one({"Questions._id":ObjectId(key)}):
                reponses.append({"question_id":key,"reponse":value.strip()})
        dictValidate["formulaire_id"] = uuid
        try:
            collection.insert_one({"sondage_id":uuid,"reponses":reponses})
            request.session['success'] = 'Your answer was registed.'
            return redirect('/home',)
        except Exception as e:
            print("Erreur lors de l'insertion dans MongoDB:", e)
            return HttpResponse("Erreur lors de l'insertion des données.", status=500)
    elif request.method == 'GET':
        if uuid is not None:
            return redirect('/form/'+uuid, {"page_title": "Home"})
        return redirect('/home', {"page_title": "Home"})


def update(request,uuid):
    if request.method == 'POST':
        form_data = request.POST
        dictValidate = {}
        Questions = []
        dictForm = {
            key: form_data.getlist(key) if len(form_data.getlist(key)) > 1 else form_data.get(key)
            for key in form_data.keys()
        }
        for key, value in dictForm.items():
            if key.startswith(('question')):  # ', 'reponse', 'form_title', 'form_description','form_password')):
                if key.startswith('questionMultiple'):
                    Questions.append({"_id": ObjectId(), "intitule": value.strip(), "type": "multiple",
                                      "reponses": dictForm["reponse" + key[len("questionMultiple"):]]})
                else:
                    Questions.append({"_id": ObjectId(), "intitule": value.strip(), "type": "unique"})

        try:
            db = MongoClient().get_database("base_formulaires")
            collection = db["Formulaires"]

            result = collection.update_one({"_id":ObjectId(uuid)},{'$set':{"nom": dictForm["form_title"], "description": dictForm["form_description"],
                                 "Questions": Questions}})
            if result.matched_count == 0:
                request.session['error'] = 'Le formulaire n\'existe pas.'
                return redirect('/home')
            else:
                request.session['success'] = 'Votre formulaire a été mis a jour.'
            return redirect('/home')
        except Exception as e:
            print("Erreur lors de l'insertion dans MongoDB:", e)
            return HttpResponse("Erreur lors de l'insertion des données.", status=500)

    elif request.method == 'GET':
        if uuid is not None:
            return redirect('/form/' + uuid, {"page_title": "Accueil"})
        return redirect('/home', {"page_title": "Accueil"})


def delete_form(request,uuid):
    if request.method == 'POST':
        form_data = request.POST
        db = MongoClient().get_database("base_formulaires")
        collection = db["Formulaires"]
        f = collection.find_one(ObjectId(uuid))
        dictForm = dict(f)
        form = FormModel(uuid, dictForm["Questions"], dictForm["nom"], dictForm["description"],
                         dictForm["password"].strip())
        if form_data["password"].strip() == form.password:
            result = collection.delete_one({"_id": ObjectId(uuid)})
            if result.deleted_count == 0:
                request.session['error'] = 'Le formulaire n\'existe pas.'
                return redirect('/home')
            else:
                request.session['success'] = 'Votre formulaire a été supprimé.'
            return redirect('/home')
        else:
            request.session['error'] = 'Le mot de passe est invalide.'
            return redirect('/home')
    return render(request, '404.html', {"page_title": "Cette page n'existe pas."}, status=404)