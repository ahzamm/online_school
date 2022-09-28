import subprocess

# subprocess.run(["export", "DJANGO_SETTINGS_MODULE=school.settings"])

from secrets import choice
import django


django.setup()
from accounts.models.student_models import StudentMore
from accounts.models import Student, Admin, User, Teacher
from classes.models import Course, Classes
import datetime

import random

User.objects.all().delete()
Course.objects.all().delete()
Classes.objects.all().delete()

print("============== DATA DELETED ==============")


c1 = "echo"
c2 = "User.objects.create_superuser(email='superuser@test.com',name='ahzam',password='1234')"
c3 = "|"
c4 = "python3"
c5 = "manage.py"
c6 = "shell_plus"
# subprocess.run([c1, c2, c3, c4, c5])

print("============== SUPER USER CREATED ==============")


for i in range(10):
    admin = Admin.objects.create_user(
        email=f"admin{i}@test.com",
        name=f"Admin {i}",
        password="1234",
    )
    admin.save()

print("============== ADMIN CREATED ==============")

teachers = []
for i in range(30):
    teacher = Teacher.objects.create_user(
        email=f"teacher{i}@test.com",
        name=f"Teacher {i}",
        password="1234",
    )
    teacher.save()
    teachers.append(teacher)

print("============== TEACHER CREATED ==============")


# Create Level 1 Courses
ch = [
    Course.CH.THREE,
    Course.CH.FOUR,
]
for i in range(40):
    Course.objects.create(
        name=f"Test Course {i}",
        course_code=f"TC {i}",
        ch=random.choice(ch),
    )

print("============== LEVEL 1 COURSE COMPLETED ==============")

# Create Level 2 Courses
lvl_1_courses = Course.objects.all()
lvl_2_courses = []
for i in range(41, 65):
    course = Course.objects.create(
        name=f"Test Course {i}",
        course_code=f"TC {i}",
        ch=random.choice(ch),
    )
    course.save()
    course.pre_req_courses.add(random.choice(lvl_1_courses))
    course.pre_req_courses.add(random.choice(lvl_1_courses))
    course.pre_req_courses.add(random.choice(lvl_1_courses))
    course.save()
    lvl_2_courses.append(course)

print("============== LEVEL 2 COURSE COMPLETED ==============")

# Create Level 3 Courses
lvl_3_courses = []
for i in range(66, 80):
    course = Course.objects.create(
        name=f"Test Course {i}",
        course_code=f"TC {i}",
        ch=random.choice(ch),
    )
    course.save()
    course.pre_req_courses.add(random.choice(lvl_2_courses))
    course.pre_req_courses.add(random.choice(lvl_2_courses))
    course.pre_req_courses.add(random.choice(lvl_2_courses))
    course.save()
    lvl_3_courses.append(course)

print("============== LEVEL 3 COURSE COMPLETED ==============")
# Create Level 4 Courses
lvl_4_courses = []
for i in range(80, 90):
    course = Course.objects.create(
        name=f"Test Course {i}",
        course_code=f"TC {i}",
        ch=random.choice(ch),
    )
    course.save()
    course.pre_req_courses.add(random.choice(lvl_3_courses))
    course.pre_req_courses.add(random.choice(lvl_3_courses))
    course.pre_req_courses.add(random.choice(lvl_3_courses))
    course.save()
    lvl_4_courses.append(course)


print("============== LEVEL 4 COURSE COMPLETED ==============")


grade = [
    StudentMore.Grade.ONE,
    StudentMore.Grade.TWO,
    StudentMore.Grade.THREE,
    StudentMore.Grade.FOURE,
    StudentMore.Grade.FIVE,
]
# Create level 1 Students
lvl_1_students = []
for i in range(400):

    student = Student.objects.create_user(
        email=f"student{i}@test.com",
        name=f"Student {i}",
        password="1234",
    )
    student.save()
    lvl_1_students.append(student)

    studentmore = StudentMore.objects.create(
        user=student,
        grade=random.choice(grade),
        roll_no=f"roll_no_{i}",
    )
    studentmore.cleared_course.add(random.choice(lvl_1_courses))
    studentmore.cleared_course.add(random.choice(lvl_1_courses))
    studentmore.cleared_course.add(random.choice(lvl_1_courses))
    studentmore.cleared_course.add(random.choice(lvl_1_courses))
    studentmore.cleared_course.add(random.choice(lvl_1_courses))
    studentmore.save()


print("============== LEVEL 1 STUDENT COMPLETED ==============")

# Create level 2 Students
lvl_2_students = []
for i in range(401, 600):

    student = Student.objects.create_user(
        email=f"student{i}@test.com",
        name=f"Student {i}",
        password="1234",
    )
    student.save()
    lvl_2_students.append(student)

    studentmore = StudentMore.objects.create(
        user=student,
        grade=random.choice(grade),
        roll_no=f"roll_no_{i}",
    )
    studentmore.cleared_course.add(random.choice(lvl_2_courses))
    studentmore.cleared_course.add(random.choice(lvl_2_courses))
    studentmore.cleared_course.add(random.choice(lvl_2_courses))
    studentmore.cleared_course.add(random.choice(lvl_2_courses))
    studentmore.cleared_course.add(random.choice(lvl_2_courses))
    studentmore.save()


print("============== LEVEL 2 STUDENT COMPLETED ==============")

# Create level 3 Students
lvl_3_students = []
for i in range(601, 800):

    student = Student.objects.create_user(
        email=f"student{i}@test.com",
        name=f"Student {i}",
        password="1234",
    )
    student.save()
    lvl_3_students.append(student)

    studentmore = StudentMore.objects.create(
        user=student,
        grade=random.choice(grade),
        roll_no=f"roll_no_{i}",
    )
    studentmore.cleared_course.add(random.choice(lvl_3_courses))
    studentmore.cleared_course.add(random.choice(lvl_3_courses))
    studentmore.cleared_course.add(random.choice(lvl_3_courses))
    studentmore.cleared_course.add(random.choice(lvl_3_courses))
    studentmore.cleared_course.add(random.choice(lvl_3_courses))
    studentmore.save()


print("============== LEVEL 3 STUDENT COMPLETED ==============")

# Create level 4 Students
lvl_4_students = []
for i in range(801, 1000):

    student = Student.objects.create_user(
        email=f"student{i}@test.com",
        name=f"Student {i}",
        password="1234",
    )
    student.save()
    lvl_4_students.append(student)

    studentmore = StudentMore.objects.create(
        user=student,
        grade=random.choice(grade),
        roll_no=f"roll_no_{i}",
    )
    studentmore.cleared_course.add(random.choice(lvl_4_courses))
    studentmore.cleared_course.add(random.choice(lvl_4_courses))
    studentmore.cleared_course.add(random.choice(lvl_4_courses))
    studentmore.cleared_course.add(random.choice(lvl_4_courses))
    studentmore.cleared_course.add(random.choice(lvl_4_courses))
    studentmore.save()


print("============== LEVEL 4 STUDENT COMPLETED ==============")


sections = [Classes.SECTION.A, Classes.SECTION.B, Classes.SECTION.C]

# create level 1 classes

for _ in range(20):
    _class = Classes.objects.create(
        course=random.choice(lvl_1_courses),
        teacher=random.choice(teachers),
        section=random.choice(sections),
        enrollment_start_date=datetime.date.today(),
        enrollment_end_date=datetime.date.today(),
        mid_exammination_date=datetime.date.today(),
        final_exammination_date=datetime.date.today(),
    )

    for _ in range(50):
        _class.student.add(random.choice(lvl_1_students))

print("============== LEVEL 1 CLASSES CREATED ==============")


for _ in range(20):
    _class = Classes.objects.create(
        course=random.choice(lvl_2_courses),
        teacher=random.choice(teachers),
        section=random.choice(sections),
        enrollment_start_date=datetime.date.today(),
        enrollment_end_date=datetime.date.today(),
        mid_exammination_date=datetime.date.today(),
        final_exammination_date=datetime.date.today(),
    )

    for _ in range(50):
        _class.student.add(random.choice(lvl_2_students))
print("============== LEVEL 2 CLASSES CREATED ==============")

for _ in range(20):
    _class = Classes.objects.create(
        course=random.choice(lvl_3_courses),
        teacher=random.choice(teachers),
        section=random.choice(sections),
        enrollment_start_date=datetime.date.today(),
        enrollment_end_date=datetime.date.today(),
        mid_exammination_date=datetime.date.today(),
        final_exammination_date=datetime.date.today(),
    )

    for _ in range(50):
        _class.student.add(random.choice(lvl_3_students))
print("============== LEVEL 3 CLASSES CREATED ==============")

for _ in range(20):
    _class = Classes.objects.create(
        course=random.choice(lvl_4_courses),
        teacher=random.choice(teachers),
        section=random.choice(sections),
        enrollment_start_date=datetime.date.today(),
        enrollment_end_date=datetime.date.today(),
        mid_exammination_date=datetime.date.today(),
        final_exammination_date=datetime.date.today(),
    )

    for _ in range(50):
        _class.student.add(random.choice(lvl_4_students))
print("============== LEVEL 4 CLASSES CREATED ==============")
