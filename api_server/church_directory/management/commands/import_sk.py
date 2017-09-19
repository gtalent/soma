#! /usr/bin/env python3

import csv
import datetime
import os
import shutil
import sys
from os.path import join

from django.db.models import Q
from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django_resized import ResizedImageField
from soma.settings import MEDIA_ROOT
from church_directory.models import Event, EventType, RoleAssignment, Role, Person, sex_int
from church_directory.models import NON_MEMBER, MEMBER
from church_directory.models import PERSON_PICTURE_WIDTH, PERSON_PICTURE_HEIGHT, PERSON_PICTURE_DIR, MALE, _crop_image
from church_directory.models import EVENT_BAPTISM, EVENT_DEATH, EVENT_LEFT_CHURCH, EVENT_WEDDING

EVENT_TYPES = {}

for t in EventType.objects.all():
    EVENT_TYPES[t.name] = t

PICTURE_DIR = MEDIA_ROOT + '/' + PERSON_PICTURE_DIR
BLANK_DATE = '  /  /    '

def member_status(s):
    if s == 'Active Member':
        return MEMBER
    elif s == 'Homebound Member':
        return MEMBER
    elif s == 'Out-of-the-area Member':
        return MEMBER
    else:
        return NON_MEMBER

def homebound(s):
    if s == 'Homebound Member':
        return True
    else:
        return False

def out_of_area(s):
    if s == 'Out-of-the-area Member':
        return True
    else:
        return False

def parse_date(d):
    try:
        d = d.split('/')
        month = int(d[0])
        day = int(d[1])
        year = int(d[2])
        return datetime.date(year, month, day)
    except ValueError:
        return None

def fix_phone(number):
    out = ''
    for v in number:
        if v >= '0' and v <= '9':
            out += v
    if len(out) != 10:
        out = None
    return out

def add_role(person, name):
    try:
        rt = Role.objects.get(name=name)
    except Role.DoesNotExist:
        rt = Role(name=name)
        rt.save()
    r = RoleAssignment(role_type=rt, person=person)
    etf = Q(event_type=EVENT_TYPES[EVENT_LEFT_CHURCH]) | Q(event_type=EVENT_TYPES[EVENT_DEATH])
    events = Event.objects.filter(person=person).filter(etf).order_by('date')
    if len(events):
        r.end_date = events[0].date
    r.save()

class Command(BaseCommand):
    help = 'Imports a CSV file of Persons'

    def add_arguments(self, parser):
        parser.add_argument('in', nargs='+', type=str)

    def handle(self, *args, **options):
        families = {}
        # clear Persons
        Person.objects.all().delete()
        Role.objects.all().delete()
        # import new Persons
        path = options['in'][0]
        data_dir = os.path.dirname(os.path.realpath(path))
        with open(path) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            i = 1
            for row in reader:
                i += 1
                sex = sex_int(row['Gender'])
                if sex != None:
                    p = Person()
                    p.first_name = row['First Name']
                    p.middle_name = row['Middle Name']
                    p.last_name = row['Last Name']
                    p.suffix = row['Suffix']
                    if row['Marital Status'] == 'Married':
                        p.marital_status = 2
                    else:
                        p.marital_status = 1
                    p.sex = sex
                    p.home_phone = fix_phone(row['Home Phone'])
                    p.cell_phone = fix_phone(row['Cell Phone'])
                    p.email_address = row['E-Mail']
                    p.address_line1 = row['Address']
                    p.address_line2 = row['Address Line 2']
                    p.city = row['City']
                    p.zipcode = row['Zip Code']
                    p.province = row['State']
                    ms = row['Member Status']
                    p.member = member_status(ms)
                    p.homebound = homebound(ms)
                    p.out_of_area = out_of_area(ms)
                    p.notes = row['Comments']
                    rel = row['Relationship']
                    p.birthday = parse_date(row['Birth Date'])
                    if i % 50 == 0:
                        sys.stdout.write('\rPerson: ' + str(i))
                        sys.stdout.flush()
                    fam_name = row['Directory Name']
                    if not fam_name in families:
                        families[fam_name] = {
                            'father': None,
                            'mother': None,
                            'children': [],
                        }
                    if rel == 'Son' or rel == 'Daughter':
                        families[fam_name]['children'].append(p)
                    elif rel == 'Spouse' or rel == 'head of household':
                        if p.sex == MALE:
                            families[fam_name]['father'] = p
                        else:
                            families[fam_name]['mother'] = p
                    p.save()

                    # setup associations that cannot be performed before the
                    # person is in the database

                    # create Events
                    for et in [
                        ('Baptized Date', EVENT_BAPTISM),
                        ('Deceased date', EVENT_DEATH),
                        ('Date Removed', EVENT_LEFT_CHURCH),
                        ('Wedding Date', EVENT_WEDDING),
                    ]:
                        dk = et[0]
                        tk = et[1]
                        bd = parse_date(row[dk])
                        if bd != None:
                            e = Event(person=p, event_type=EVENT_TYPES[tk], date=bd)
                            e.save()
                    # setup roles
                    roles = row['Leadership'].split('; ')
                    for role in roles:
                        if role != '':
                            add_role(p, role)
                    # import picture
                    src = join(data_dir, p.last_name + ', ' + p.first_name + '.jpg')
                    try:
                        dest = join(PICTURE_DIR, str(p.person_id) + '.jpg')
                        shutil.copyfile(src, dest)
                        _crop_image(dest, PERSON_PICTURE_WIDTH, PERSON_PICTURE_HEIGHT)
                        p.picture = PERSON_PICTURE_DIR + '/' + str(p.person_id) + '.jpg'
                        p.save()
                    except IOError:
                        pass
            sys.stdout.write('\rPerson: ' + str(i) + '\n')
            sys.stdout.flush()
            i = 0
            for k in families:
                f = families[k]
                for c in f['children']:
                    if i % 50 == 0:
                        sys.stdout.write('\rParent-child relationship: ' + str(i))
                        sys.stdout.flush()
                    c.father = f['father']
                    c.mother = f['mother']
                    c.save()
                    i += 1
            sys.stdout.write('\rParent-child relationship: ' + str(i) + '\n')
            sys.stdout.flush()
