"""
URL configuration for ProjetFinalnosql project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from ProjetFinalnosql import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', views.home, name='home'),
path('', views.home, name='home'),
path('create/form/', views.create_form, name='form'),
path('update/form/<str:uuid>', views.form_as_admin, name='form'),
path('Delete/form/<str:uuid>', views.delete_form, name='form'),
path('updateValidate/form/<str:uuid>', views.update, name='form'),
path('answer/<str:uuid>', views.answer_form, name='answer'),
path('form/<str:uuid>', views.form, name='answer')
]
