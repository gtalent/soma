import os
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import Context, loader
import weasyprint
from datetime import datetime
from .models import Person, membership_status_str, sex_str, PERSON_PICTURE_DIR
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
	now = datetime.now()
	for p in people:
		p.membership_status = membership_status_str(p.membership_status)
	t = loader.get_template(SOMA_HOME + '/templates/church_directory.html')
	c = Context({
		'people': people,
		'church_name': CHURCH_NAME,
		'month_name': now.strftime('%B'),
		'year': now.year
	})
	html_doc = t.render(c)
	#return HttpResponse(html_doc)
	pdf_doc = weasyprint.HTML(string=html_doc, url_fetcher=_person_image_fetch).write_pdf()

	response = HttpResponse(pdf_doc, content_type='application/pdf')
	response['Content-Disposition'] = 'filename="Church_Directory.pdf"'

	return response

@login_required
def directory_page(rqst):
	people = Person.objects.all().order_by('last_name', 'first_name')
	out = []
	for p in people:
		out.append({
			'person_id': p.person_id,
			'first_name': p.first_name,
			'middle_name': p.middle_name,
			'last_name': p.last_name,
			'suffix': p.suffix,
			'sex': sex_str(p.sex),
			'birthday': str(p.birthday),
			'home_number': p.home_number,
			'cell_number': p.cell_number,
			'email_address': p.email_address,
			'address': {
				'address_line1': p.address_line1,
				'address_line2': p.address_line2,
				'unit_number': p.unit_number,
			},
			'membership_status': membership_status_str(p.membership_status),
			'father': p.father.person_id if p.father else None,
			'mother': p.mother.person_id if p.mother else None,
		})
	response = HttpResponse(json.dumps(out, indent=3), content_type='application/json')
	return response
