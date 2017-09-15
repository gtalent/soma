#! /usr/bin/env python3

import csv
import datetime
import os
import shutil
import sys
from os.path import join

from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from django_resized import ResizedImageField
from soma.settings import MEDIA_ROOT
from church_directory.models import Person, sex_int, membership_status_str, NON_MEMBER, ACTIVE_MEMBER, HOMEBOUND_MEMBER, OUTOFAREA_MEMBER, FORMER_MEMBER, DECEASED, PERSON_PICTURE_WIDTH, PERSON_PICTURE_HEIGHT, PERSON_PICTURE_DIR, MALE, _crop_image

PICTURE_DIR = MEDIA_ROOT + '/' + PERSON_PICTURE_DIR

def member_status(s):
    if s == 'Active Member':
        return ACTIVE_MEMBER
    elif s == 'Homebound Member':
        return HOMEBOUND_MEMBER
    elif s == 'Out-of-the-area Member':
        return OUTOFAREA_MEMBER
    elif s == 'Former Member':
        return FORMER_MEMBER
    else:
        return NON_MEMBER

def birthday(row):
    try:
        d = row['Birth Date'].split('/')
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

class Command(BaseCommand):
    help = 'Imports a CSV file of Persons'

    def add_arguments(self, parser):
        parser.add_argument('in', nargs='+', type=str)

    def handle(self, *args, **options):
        families = {}
        # clear Persons
        Person.objects.all().delete()
        # import new Persons
        path = options['in'][0]
        data_dir = os.path.dirname(os.path.realpath(path))
        with open(path) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            i = 1
            for row in reader:
                i += 1
                if len(row) > 0:
                    p = Person()
                    p.first_name = row['First Name']
                    p.middle_name = row['Middle Name']
                    p.last_name = row['Last Name']
                    p.suffix = row['Suffix']
                    if row['Marital Status'] == 'Married':
                        p.marital_status = 2
                    else:
                        p.marital_status = 1
                    p.sex = sex_int(row['Gender'])
                    p.home_phone = fix_phone(row['Home Phone'])
                    p.cell_phone = fix_phone(row['Cell Phone'])
                    p.email_address = row['E-Mail']
                    p.address_line1 = row['Address']
                    p.address_line2 = row['Address Line 2']
                    p.membership_status = member_status(row['Member Status'])
                    p.notes = row['Comments']
                    rel = row['Relationship']
                    p.birthday = birthday(row)
                    if i % 50 == 0:
                        sys.stdout.write('\rPerson: ' + str(i))
                        sys.stdout.flush()
                    if p.sex != None:
                        fam_name = row['Directory Name']
                        if not fam_name in families:
                            families[fam_name] = {
                                'father': None,
                                'mother': None,
                                'children': [],
                            }
                        if rel == 'Son' or rel == 'Daughter':
                            families[fam_name]['children'].append(p)
                        elif p.sex == MALE:
                            families[fam_name]['father'] = p
                        else:
                            families[fam_name]['mother'] = p
                        p.save()
                        src = join(data_dir, p.last_name + ', ' + p.first_name + '.jpg')
                        try:
                            dest = join(PICTURE_DIR, str(p.person_id) + '.jpg')
                            shutil.copyfile(src, dest)
                            _crop_image(dest, PERSON_PICTURE_WIDTH, PERSON_PICTURE_HEIGHT)
                        except IOError:
                            continue
                        p.picture = PERSON_PICTURE_DIR + '/' + str(p.person_id) + '.jpg'
                        p.save()
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
            sys.stdout.write("\r" + str(k))
            sys.stdout.flush()
            print()
    # father
    # mother
    # spouse
    # notes
    # birthday
