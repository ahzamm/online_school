from accounts.models import Student, Teacher, User
from classes.models import Attendence, Classes, Course, TimeTable


for i in range(1000):
    Student.objects.create(
        email=f"student{i}@test.com",
        name=f"Student {i}",
    )
