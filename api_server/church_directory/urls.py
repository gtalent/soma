
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^church_directory.pdf', views.church_directory_pdf),
    url(r'^directory_page', views.directory_page),
    url(r'^group_stat', views.group_stat),
    url(r'^person', views.person),
]
