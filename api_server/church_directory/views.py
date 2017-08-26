
import json
import os
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
import weasyprint
from datetime import datetime
from .models import Person, membership_status_int, membership_status_str, sex_str, PERSON_PICTURE_DIR
from soma.settings import CHURCH_NAME, SOMA_HOME, MEDIA_ROOT

def _person_image_fetch(url):
	prefix = 'image://'
	if url.startswith(prefix):
		url = 'file://' + os.path.abspath(MEDIA_ROOT + url[len(prefix):])
	return weasyprint.default_url_fetcher(url)

def _build_membership_filter(ms):
    filt = None
    for i in ms:
        q = Q(membership_status=membership_status_int(i))
        if filt == None:
            filt = q
        else:
            filt = filt | q
    return filt if filt != None else Q()

def _delimit_phone_number(num):
    if num != None and len(num) == 10:
        return '(' + num[:3] + ') ' + num[3:6] + '-' + num[6:10]

def _jsonify_person(person):
    return {
        'image_url': person.picture.url if person.picture else None,
        'person_id': person.person_id,
        'first_name': person.first_name,
        'middle_name': person.middle_name,
        'last_name': person.last_name,
        'suffix': person.suffix,
        'sex': sex_str(person.sex),
        'birthday': str(person.birthday),
        'home_number': _delimit_phone_number(person.home_phone),
        'cell_number': _delimit_phone_number(person.cell_phone),
        'email_address': person.email_address,
        'address': {
            'address_line1': person.address_line1,
            'address_line2': person.address_line2,
        },
        'membership_status': membership_status_str(person.membership_status),
        'father': person.father.person_id if person.father else None,
        'mother': person.mother.person_id if person.mother else None,
    }

# Create your views here.

@login_required
def church_directory_pdf(rqst):
    if rqst.method == 'GET':
        people = Person.objects.all().order_by('last_name', 'first_name')
        now = datetime.now()
        for p in people:
                p.membership_status = membership_status_str(p.membership_status)
        t = loader.get_template(SOMA_HOME + '/templates/church_directory.html')
        c = {
            'people': people,
            'church_name': CHURCH_NAME,
            'month_name': now.strftime('%B'),
            'year': now.year
        }
        html_doc = t.render(c)
        pdf_doc = weasyprint.HTML(string=html_doc, url_fetcher=_person_image_fetch).write_pdf()

        response = HttpResponse(pdf_doc, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="Church_Directory.pdf"'

        return response
    return HttpResponse(status=404)

@login_required
def directory_page(rqst):
    if rqst.method == 'POST':
        data = json.loads(rqst.body)
        try:
            ms = data['membership_status']
        except KeyError:
            return HttpResponse(json.dumps([], indent=3), content_type='application/json')
        filt = _build_membership_filter(ms)
        people = Person.objects.filter(filt).order_by('last_name', 'first_name')
        try:
            start = data['start']
        except KeyError:
            start = 0
        try:
            end = data['end']
        except KeyError:
            end = len(people)
        people = people[start:end]
        out = []
        for p in people:
            out.append(_jsonify_person(p))
        return HttpResponse(json.dumps(out, indent=3), content_type='application/json')
    else:
        return HttpResponse(status=404)

@login_required
def group_stat(rqst):
    if rqst.method == 'POST':
        data = json.loads(rqst.body)
        try:
            ms = data['membership_status']
        except KeyError:
            return HttpResponse(json.dumps([], indent=3), content_type='application/json')
        filt = _build_membership_filter(ms)
        people = Person.objects.filter(filt)
        out = {
            'group_size': len(people),
        }
        return HttpResponse(json.dumps(out, indent=3), content_type='application/json')
    return HttpResponse(status=404)

@login_required
def person(rqst):
    if rqst.method == 'POST':
        data = json.loads(rqst.body)
        person_id = None
        try:
            person_id = data['person_id']
        except KeyError:
            return HttpResponse(status=404)
        q = Person.objects.filter(person_id=person_id)
        if len(q) > 0:
            out = _jsonify_person(q[0])
            return HttpResponse(json.dumps(out, indent=3), content_type='application/json')
    return HttpResponse(status=404)
