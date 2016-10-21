from django.db import models

PERSON_PICTURE_DIR = 'upload/church_directory/person/pictures'

# Create your models here.

class Person(models.Model):
	person_id = models.AutoField("ID", primary_key=True)
	first_name = models.CharField('First Name', max_length=50)
	last_name = models.CharField('Last Name', max_length=50)
	picture = models.ImageField(upload_to=PERSON_PICTURE_DIR)
	is_member = models.BooleanField(default=False)

	class Meta:
		verbose_name_plural = 'People'

	def __unicode__(self):
		return self.first_name + ' ' + self.last_name

class MembershipStatusChange(models.Model):
   person = models.IntegerField(primary_key=True)
   begin_date = models.DateField()
   end_date = models.DateField(null=True)
