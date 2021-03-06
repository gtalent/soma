from django.contrib import admin
from church_directory.models import Clearance, ClearanceType, Event, EventType, Person, RoleAssignment, Role, MembershipStatusChange

# Register your models here.

class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'member', 'birthday', 'sex', 'marital_status')
    def row_name(self, p):
        return p.last_name + ', ' + p.first_name
    row_name.short_description = 'Name'
    row_name.admin_order_field = 'last_name'

class RoleAssignmentAdmin(admin.ModelAdmin):
    list_display = ('person', 'role_name', 'start_date', 'end_date')
    def row_name(self, p):
        return p.role_name + ': ' + p.last_name + ', ' + p.first_name
    row_name.short_description = 'Name'
    row_name.admin_order_field = 'person__last_name'

admin.site.register(Clearance)
admin.site.register(ClearanceType)
admin.site.register(Event)
admin.site.register(EventType)
admin.site.register(Person, PersonAdmin)
admin.site.register(RoleAssignment, RoleAssignmentAdmin)
admin.site.register(Role)
