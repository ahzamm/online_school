from accounts.models import Admin, Student, Teacher, User
from classes.models import Attendence, Classes, Course, TimeTable


for i in range(1000):
    Student.objects.create()
