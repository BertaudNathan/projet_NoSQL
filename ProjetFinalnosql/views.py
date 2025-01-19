from django.forms import forms, Form
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from pymongo import MongoClient
from pymongo.synchronous.collection import Collection

from ProjetFinalnosql.db import MongoDBDatabase
from ProjetFinalnosql.model.myForm import MyForm


def home(request):
    return render(request, 'home.html', {"page_title": "Home"})


def form(request,uuid):
    db = MongoDBDatabase("mongodb://localhost:27017/","base_formulaires")
    col = db.database.get_collection("test_collection")
    print(col.find({}))
    return render(request, 'form.html', {"page_title": "Answer a form", "collection":db.find(col, {"nom": "et oui"})})

def create_form(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            try:
                # Connexion à MongoDB
                db = MongoClient().get_database("base_formulaires")
                collection = db["Formulaires"]

                # Insérer les données nettoyées dans MongoDB
                collection.insert_one(cleaned_data)
                return HttpResponse("Formulaire soumis avec succès.")
            except Exception as e:
                print("Erreur lors de l'insertion dans MongoDB:", e)
                return HttpResponse("Erreur lors de l'insertion des données.", status=500)
        else:
            print("Form is not valid")
            print(form)
            return HttpResponse(form)

        return HttpResponse("Form submitted")



    elif request.method == 'GET':
        return render(request, 'create_form.html', {"page_title": "Create a form"})


def form_as_admin(request,uuid):
    # get data

    return render(request, 'form.html', {"page_title": "Poll"})
