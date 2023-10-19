from django.contrib import admin
from django.urls import path,include
from qbecapp import views

urlpatterns = [
    path("",views.base,name="base"),
    path("card/",views.card,name="card"),
    # path("/result",views.card,name="card"),
]
