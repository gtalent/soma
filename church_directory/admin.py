from django.contrib import admin
from church_directory.models import Person, MembershipStatusChange

# Register your models here.

class PersonAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'membership_status', 'birthday', 'sex')
	def row_name(self, p):
		return p.last_name + ', ' + p.first_name
	row_name.short_description = 'Name'
	row_name.admin_order_field = 'last_name'

admin.site.register(Person, PersonAdmin)
