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
from ProjetFinalnosql.model.FormModel import FormModel
from ProjetFinalnosql.model.myForm import MyForm


def home(request):
    print(request.session)
    if 'success' in request.session:
        success = request.session['success']
        del request.session['success']
        return render(request, 'home.html', {"page_title": "Home", "success": success})
    elif 'error' in request.session:
        error = request.session['error']
        del request.session['error']
        return render(request, 'home.html', {"page_title": "Home", "error": error})
    elif 'info' in request.session:
        info = request.session['info']
        del request.session['info']
        return render(request, 'home.html', {"page_title": "Home", "info": info})
    return render(request, 'home.html', {"page_title": "Home"})


def form(request,uuid):
    print(uuid)
    db = MongoClient().get_database("base_formulaires")
    collection = db["Formulaires"]
    dictForm = collection.find_one(ObjectId(uuid))
    dictForm = dict(dictForm)
    QuestionsReponses = {}
    for key, value in dictForm.items():
        if key.startswith("questionMultiple"):
            # Extraire le numéro après "question"
            num = key[len("questionMultiple"):]
            response_key = f"reponse{num}"  # Construire la clé réponse correspondante

            if response_key in dictForm:  # Vérifier si la réponse correspondante existe
                QuestionsReponses[value] = dictForm[response_key]
        elif key.startswith("question"):
            # Extraire le numéro après "question"
            num = key[len("question"):]
            response_key = f"reponse{num}"  # Construire la clé réponse correspondante

            if response_key in dictForm:  # Vérifier si la réponse correspondante existe
                QuestionsReponses[value] = dictForm[response_key]
            else:
                QuestionsReponses[value] = None

    print(QuestionsReponses)
    form = FormModel(uuid,QuestionsReponses,dictForm["form_title"],dictForm["form_description"],dictForm["form_password"])
    return render(request, 'form.html', {"page_title": "Answer a form", "form": form, "uuid": uuid})

def create_form(request):
    if request.method == 'POST':
        form_data = request.POST
        dictValidate={}
        dictForm = {
            key: form_data.getlist(key) if len(form_data.getlist(key)) > 1 else form_data.get(key)
            for key in form_data.keys()
        }
        for key, value in dictForm.items():
            if key.startswith(('question', 'reponse', 'form_title', 'form_description','form_password')):
                dictValidate[key.replace("[","").replace("]","")] = value.trim()
        try:
            db = MongoClient().get_database("base_formulaires")
            collection = db["Formulaires"]
            collection.insert_one(dictValidate)
            request.session['success'] = 'Your answer was registed.'
            return redirect('/')
        except Exception as e:
            print("Erreur lors de l'insertion dans MongoDB:", e)
            return HttpResponse("Erreur lors de l'insertion des données.", status=500)




    elif request.method == 'GET':
        return render(request, 'create_form.html', {"page_title": "Create a form"})


def form_as_admin(request,uuid):
    # get data

    return render(request, 'form.html', {"page_title": "Update a form"})


def answer_form(request,uuid):
    if request.method == 'POST':
        if uuid is None:
            return render(request, '404.html', {"page_title": "This page does not exist."}, status=404)
        form_data = request.POST
        print(form_data)
        dictValidate={}
        dictForm = {
            key: form_data.getlist(key) if len(form_data.getlist(key)) > 1 else form_data.get(key)
            for key in form_data.keys()
        }
        for key, value in dictForm.items():
            if key.startswith('reponse'):
                dictValidate[key] = value.strip()
        dictValidate["formulaire_id"] = uuid
        try:
            db = MongoClient().get_database("base_formulaires")
            collection = db["Reponses"]
            collection.insert_one(dictValidate)
            #print(dictValidate)
            request.session['success'] = 'Your answer was registed.'

            return redirect('/',)
        except Exception as e:
            print("Erreur lors de l'insertion dans MongoDB:", e)
            return HttpResponse("Erreur lors de l'insertion des données.", status=500)



    elif request.method == 'GET':
        if uuid is not None:
            return redirect('/form/'+uuid, {"page_title": "Home"})
        return redirect('/', {"page_title": "Home"})
