from bson import ObjectId
from django.forms import forms, Form, ModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from pymongo import MongoClient
from pymongo.synchronous.collection import Collection
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, render

from ProjetFinalnosql.db import MongoDBDatabase
from ProjetFinalnosql.model.AnswerModel import AnswerModel
from ProjetFinalnosql.model.FormModel import FormModel
from ProjetFinalnosql.model.QuestionModel import QuestionModel



def home(request):
    print("------------------------------------------------------------------------")
    db = MongoClient().get_database("base_formulaires")
    collection = db["Formulaires"]
    forms = collection.find({}).to_list();
    for i in forms:
        i["id"] = str(i["_id"])
    if 'success' in request.session:
        success = request.session['success']
        del request.session['success']
        return render(request, 'home.html', {"page_title": "Home", "success": success, "forms": forms})
    elif 'error' in request.session:
        error = request.session['error']
        del request.session['error']
        return render(request, 'home.html', {"page_title": "Home", "error": error, "forms": forms})
    elif 'info' in request.session:
        info = request.session['info']
        del request.session['info']
        return render(request, 'home.html', {"page_title": "Home", "info": info, "forms": forms})
    print(forms)
    return render(request, 'home.html', {"page_title": "Home", "forms": forms})


def form(request,uuid):
    db = MongoClient().get_database("base_formulaires")
    collection = db["Formulaires"]
    dictForm = collection.find_one(ObjectId(uuid))
    if dictForm is None:
        return render(request, '404.html', {"page_title": "This page does not exist."}, status=404)
    dictForm = dict(dictForm)
    print(dictForm)
    Questions = []
    for question in dictForm["Questions"]:
        Questions.append(QuestionModel(question["_id"],question["intitule"],question["type"],question["reponses"] if question["type"] == "multiple" else None))
    form = FormModel(uuid, Questions,dictForm["nom"],dictForm["description"],dictForm["password"])
    print(form)
    return render(request, 'form.html', {"page_title": "Answer a form", "form": form, "uuid": uuid})

def create_form(request):
    if request.method == 'POST':
        form_data = request.POST
        dictValidate={}
        Questions = []
        dictForm = {
            key: form_data.getlist(key) if len(form_data.getlist(key)) > 1 else form_data.get(key)
            for key in form_data.keys()
        }
        print(dictForm)
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
            request.session['success'] = 'Your answer was registed.'
            return redirect('/home')
        except Exception as e:
            print("Erreur lors de l'insertion dans MongoDB:", e)
            return HttpResponse("Erreur lors de l'insertion des données.", status=500)




    elif request.method == 'GET':
        return render(request, 'create_form.html', {"page_title": "Create a form"})


def form_as_admin(request,uuid):
    if request.method == 'POST':
        form_data = request.POST
        db = MongoClient().get_database("base_formulaires")
        collection = db["Formulaires"]
        f = collection.find_one(ObjectId(uuid))
        dictForm = dict(f)
        print(dictForm)
        Questions = []
        for question in dictForm["Questions"]:
            Questions.append(QuestionModel(question["_id"], question["intitule"], question["type"],
                                           question["reponses"] if question["type"] == "multiple" else None))
        form = FormModel(uuid,Questions, dictForm["nom"], dictForm["description"], dictForm["password"].strip())
        print(form_data)
        print(dictForm["password"])
        if form_data["password"].strip() == form.password:
            return render(request, 'update_form.html', {"page_title": "Update a form", "form": form})
        else:
            request.session['error'] = 'The password is invalid.'
            return redirect('/home')
    return render(request, '404.html', {"page_title": "This page does not exist."}, status=404)


def answer_form(request,uuid):
    if request.method == 'POST':
        if uuid is None:
            return render(request, '404.html', {"page_title": "This page does not exist."}, status=404)
        form_data = request.POST
        print(form_data)
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
            print(reponses)
            collection.insert_one({"sondage_id":uuid,"reponses":reponses})
            #print(dictValidate)
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
        if uuid is None:
            return render(request, '404.html', {"page_title": "This page does not exist."}, status=404)
        form_data = request.POST
        print(form_data)
        dictValidate = {}
        reponses = []
        db = MongoClient().get_database("base_formulaires")
        collection = db["Reponses"]
        dictForm = {
            key: form_data.getlist(key) if len(form_data.getlist(key)) > 1 else form_data.get(key)
            for key in form_data.keys()
        }
        dictForm.pop("csrfmiddlewaretoken")

        for key, value in dictForm.items():

            if db["Formulaires"].find_one({"Questions._id": ObjectId(key)}):
                reponses.append({"question_id": key, "reponse": value.strip()})
        dictValidate["formulaire_id"] = uuid
        try:
            print(reponses)
            collection.insert_one({"sondage_id": uuid, "reponses": reponses})
            # print(dictValidate)
            request.session['success'] = 'Your answer was registed.'
            return redirect('/home', )
        except Exception as e:
            print("Erreur lors de l'insertion dans MongoDB:", e)
            return HttpResponse("Erreur lors de l'insertion des données.", status=500)
    elif request.method == 'GET':
        if uuid is not None:
            return redirect('/form/' + uuid, {"page_title": "Home"})
        return redirect('/home', {"page_title": "Home"})