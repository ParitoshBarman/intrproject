from django.contrib import admin
from django.urls import path
from intrapp import views

urlpatterns = [
    path("", views.index, name='home'),
    path("deletdata/<str:slID>/<str:token>", views.deletdata, name='deletdata'),
    path("loginSuccess", views.loginSuccess, name='loginSuccess'),
    path("update/<str:slID>/<str:token>", views.update, name='update'),
    path("updateForm/<str:slID>/<str:token>", views.updateForm, name='updateForm'),
    path("savedata/<str:token>", views.savedata, name='savedata'),
]
