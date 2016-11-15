from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import Context, loader
import weasyprint
import os
from .models import Person, membership_status_str, PERSON_PICTURE_DIR
from soma.settings import CHURCH_NAME, SOMA_HOME, MEDIA_ROOT

def _person_image_fetch(url):
	prefix = 'image://'
	if url.startswith(prefix):
		url = 'file://' + os.path.abspath(MEDIA_ROOT + url[len(prefix):])
	return weasyprint.default_url_fetcher(url)

# Create your views here.

@login_required
def church_directory_pdf(rqst):
	people = Person.objects.all().order_by('last_name', 'first_name')
	for p in people:
		p.membership_status = membership_status_str(p.membership_status)
	t = loader.get_template('church_directory/person.html')
	c = Context({'people': people, 'church_name': CHURCH_NAME})
	html_doc = t.render(c)
	#return HttpResponse(html_doc)
	pdf_doc = weasyprint.HTML(string=html_doc, url_fetcher=_person_image_fetch).write_pdf()

	response = HttpResponse(pdf_doc, content_type='application/pdf')
	response['Content-Disposition'] = 'filename="Church_Directory.pdf"'

	return response
