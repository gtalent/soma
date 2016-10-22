from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import Context, loader
from .models import Person

# Create your views here.

@login_required
def index(rqst):
	people = Person.objects.all()
	t = loader.get_template('church_directory/person.html')
	c = Context({'people': people})
	return HttpResponse(t.render(c))
