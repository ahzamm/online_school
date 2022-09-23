from django.contrib import admin

from .models import Attendence, Classes, Course, TimeTable

# Register your models here.


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_code', 'ch')


class ClassesAdmin(admin.ModelAdmin):
    list_display = ('course', 'teacher', 'enrollment_start_date',
                    'enrollment_end_date', 'section')


class AttendenceAdmin(admin.ModelAdmin):
    list_display = ('date', 'start_time', 'end_time', '_class')


class TimeTableAdmin(admin.ModelAdmin):
    list_display = ('days', 'start_time', 'end_time', 'room_no', '_class')


admin.site.register(Course, CourseAdmin)
admin.site.register(Classes, ClassesAdmin)
admin.site.register(Attendence, AttendenceAdmin)
admin.site.register(TimeTable, TimeTableAdmin)
