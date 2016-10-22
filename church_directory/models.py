from django.db import models

PERSON_PICTURE_DIR = 'upload/church_directory/person/pictures'

NON_MEMBER = 0
MEMBER = 1
FORMER_MEMBER = 2

MEMBERSHIP_STATUS = (
	 (NON_MEMBER, 'Non-member'),
	 (MEMBER, 'Member'),
	 (FORMER_MEMBER, 'Former Member'),
)

MALE = 0
FEMALE = 1

SEXES = (
	 (MALE, 'Male'),
	 (FEMALE, 'Female'),
)


# Create your models here.

class Person(models.Model):
	person_id = models.AutoField("ID", primary_key=True)
	first_name = models.CharField('First Name', max_length=50)
	last_name = models.CharField('Last Name', max_length=50)
	suffix = models.CharField('Suffix', max_length=5, null=True, blank=True)
	sex = models.IntegerField(
	    choices=SEXES,
	)
	birthday = models.DateField()
	email_address = models.CharField('Email Address', max_length=75)
	address_line1 = models.CharField('Address Line 1', max_length=50)
	address_line2 = models.CharField('Address Line 2', max_length=50, null=True, blank=True)
	apt_number = models.CharField('Apartment Number', max_length=10, null=True, blank=True)
	membership_status = models.IntegerField(
	    choices=MEMBERSHIP_STATUS,
	)
	picture = models.ImageField(upload_to=PERSON_PICTURE_DIR, null=True, blank=True)
	class Meta:
		verbose_name_plural = 'People'

	def __str__(self):
		return self.first_name + ' ' + self.last_name

class MembershipStatusChange(models.Model):
   person = models.IntegerField(primary_key=True)
   begin_date = models.DateField()
   end_date = models.DateField(null=True)
