from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^', views.church_directory_pdf),
    url(r'^church_directory.pdf', views.church_directory_pdf),
]
