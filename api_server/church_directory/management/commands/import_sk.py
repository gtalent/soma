#! /usr/bin/env python3

import csv
import datetime

from django.core.management.base import BaseCommand, CommandError
from church_directory.models import Person, sex_int, membership_status_str, NON_MEMBER, ACTIVE_MEMBER, HOMEBOUND_MEMBER, OUTOFAREA_MEMBER, FORMER_MEMBER, DECEASED

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
        c = ord(v)
        if c >= ord('0') and c <= ord('9'):
            out += v
    return out

class Command(BaseCommand):
    help = 'Imports a CSV file of Persons'

    def add_arguments(self, parser):
        parser.add_argument('in', nargs='+', type=str)

    def handle(self, *args, **options):
        # clear Persons
        Person.objects.all().delete()
        # import new Persons
        path = options['in'][0]
        with open(path) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
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
                    p.home_phone = row['Home Phone']
                    p.home_phone = fix_phone(p.home_phone)
                    if len(p.home_phone) == 0:
                        p.home_phone = None
                    p.cell_phone = row['Cell Phone']
                    p.cell_phone = fix_phone(p.cell_phone)
                    if len(p.cell_phone) == 0:
                        p.cell_phone = None
                    p.email_address = row['E-Mail']
                    p.address_line1 = row['Address']
                    p.address_line2 = row['Address Line 2']
                    p.membership_status = member_status(row['Member Status'])
                    p.notes = row['Comments']
                    p.birthday = birthday(row)
                    if p.sex != None:
                        p.save()
    # father
    # mother
    # spouse
    # notes
    # birthday
