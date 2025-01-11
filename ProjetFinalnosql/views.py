from django.forms import forms
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from pymongo.synchronous.collection import Collection

from ProjetFinalnosql.db import MongoDBDatabase


def home(request):
    return render(request, 'home.html', {"page_title": "Home"})


def form(request,uuid):
    db = MongoDBDatabase("mongodb://localhost:27017/","test")
    col = db.database.get_collection("test_collection")
    print(col.find({}))
    return render(request, 'form.html', {"page_title": "Answer a form", "collection":db.find(col, {"nom": "et oui"})})

def create_form(request):
    if request.method == 'POST':
        form = forms


    elif request.method == 'GET':
        return render(request, 'create_form.html', {"page_title": "Create a form"})


def form_as_admin(request,uuid):
    # get data

    return render(request, 'form.html', {"page_title": "Poll"})
