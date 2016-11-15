from django.db import models
from django_resized import ResizedImageField
from soma.settings import SOMA_HOME

PERSON_PICTURE_DIR = 'images/church_directory/person/pictures'

NON_MEMBER = 0
ACTIVE_MEMBER = 1
HOMEBOUND_MEMBER = 2
OUTOFAREA_MEMBER = 3
FORMER_MEMBER = 4

MEMBERSHIP_STATUS = (
	 (NON_MEMBER, 'Non-member'),
	 (ACTIVE_MEMBER, 'Active Member'),
	 (HOMEBOUND_MEMBER, 'Homebound Member'),
	 (OUTOFAREA_MEMBER, 'Out-of-area Member'),
)

def membership_status_str(status):
	if status == NON_MEMBER:
		return MEMBERSHIP_STATUS[0][1]
	elif status == ACTIVE_MEMBER:
		return MEMBERSHIP_STATUS[1][1]
	elif status == HOMEBOUND_MEMBER:
		return MEMBERSHIP_STATUS[2][1]
	elif status == OUTOFAREA_MEMBER:
		return MEMBERSHIP_STATUS[3][1]

MALE = 0
FEMALE = 1

SEXES = (
	 (MALE, 'Male'),
	 (FEMALE, 'Female'),
)


# Create your models here.

class Person(models.Model):
	person_id = models.AutoField('ID', primary_key=True)
	first_name = models.CharField('First Name', max_length=50)
	middle_name = models.CharField('Middle Name', max_length=50, null=True, blank=True)
	last_name = models.CharField('Last Name', max_length=50)
	suffix = models.CharField('Suffix', max_length=5, null=True, blank=True)
	sex = models.IntegerField(choices=SEXES)
	birthday = models.DateField()
	home_number = models.CharField('Home Number', max_length=10, blank=True, null=True)
	cell_number = models.CharField('Cell Number', max_length=10, blank=True, null=True)
	email_address = models.CharField('Email Address', max_length=75, blank=True, null=True)
	address_line1 = models.CharField('Address Line 1', max_length=50)
	address_line2 = models.CharField('Address Line 2', max_length=50, null=True, blank=True)
	unit_number = models.CharField('Apartment Number', max_length=10, null=True, blank=True)
	membership_status = models.IntegerField(choices=MEMBERSHIP_STATUS)
	father = models.ForeignKey('Person', on_delete=models.SET_NULL, related_name='father_child', null=True, blank=True)
	mother = models.ForeignKey('Person', on_delete=models.SET_NULL, related_name='mother_child', null=True, blank=True)
	picture = ResizedImageField(size=[150, 130], crop=['middle', 'center'], upload_to=PERSON_PICTURE_DIR, null=True, blank=True)

	class Meta:
		verbose_name_plural = 'People'

	def __str__(self):
		return self.first_name + ' ' + self.last_name

class MembershipStatusChange(models.Model):
	person = models.IntegerField(primary_key=True)
	begin_date = models.DateField()
	end_date = models.DateField(null=True)
