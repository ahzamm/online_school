from django.contrib import admin
from .models import *

# Register your models here.


class ClassAdmin(admin.ModelAdmin):
    list_display = ('course',)


class AttendenceAdmin(admin.ModelAdmin):
    list_display = ('_class',)


admin.site.register(Course)
admin.site.register(Classes)
admin.site.register(Attendence)
admin.site.register(TimeTable)
