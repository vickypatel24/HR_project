from django.contrib import admin

from members.models import Employee, Dep


# Register your models here.


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('f_name', 'l_name', 'age')


# admin.site.register(Employee, EmployeeAdmin)
@admin.register(Dep)
class DepAdmin(admin.ModelAdmin):
    list_display = ('id', 'dep_name', 'dep_location')

