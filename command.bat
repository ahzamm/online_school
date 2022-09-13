@REM MIGRATION AND MIGRATE
python manage.py makemigrations classes
python manage.py makemigrations accounts
python manage.py migrate


@REM CREATE SUPER USER
echo User.objects.create_superuser(email='superuser@test.com',name='ahzam',password='1234') | python manage.py shell_plus


@REM CREATE 3 ADMINS
echo Admin.objects.create_user(email="admin1@test.com", name="Admin1", password="1234") | python manage.py shell_plus
echo Admin.objects.create_user(email="admin2@test.com", name="Admin2", password="1234") | python manage.py shell_plus
echo Admin.objects.create_user(email="admin3@test.com", name="Admin3", password="1234") | python manage.py shell_plus


@REM CREATE 3 TEACHERS
echo Teacher.objects.create_user(email="teacher1@test.com", name="Teacher1", password="1234") | python manage.py shell_plus
echo Teacher.objects.create_user(email="teacher2@test.com", name="Teacher2", password="1234") | python manage.py shell_plus
echo Teacher.objects.create_user(email="teacher3@test.com", name="Teacher3", password="1234") | python manage.py shell_plus


@REM CREATE 3 STUDENTS
echo Student.objects.create_user(email="student1@test.com", name="Student1", password="1234") | python manage.py shell_plus
echo Student.objects.create_user(email="student2@test.com", name="Student2", password="1234") | python manage.py shell_plus
echo Student.objects.create_user(email="student3@test.com", name="Student3", password="1234") | python manage.py shell_plus


@REM CREATE 4 COURSES
echo Course.objects.create(name="Programming Fundamental",course_code="PF123",teacher=Teacher.objects.get(name="Teacher1"),ch=Course.CH.FOUR) | python manage.py shell_plus
echo Course.objects.create(name="Information and Communication Technology",course_code="ICT123",teacher=Teacher.objects.get(name="Teacher2"),ch=Course.CH.FOUR) | python manage.py shell_plus
echo Course.objects.create(name="Data Base Management System",course_code="DBMS123",teacher=Teacher.objects.get(name="Teacher1"),ch=Course.CH.FOUR) | python manage.py shell_plus
echo Course.objects.create(name="Arabic",course_code="ARB123",teacher=Teacher.objects.get(name="Teacher3"),ch=Course.CH.FOUR) | python manage.py shell_plus


@REM CREATE 4 CLASSES
echo from datetime import date; classes=Classes.objects.create(course=Course.objects.get(course_code="PF123"),enrollment_start_date=date.today(),enrollment_end_date=date.today()); classes.student.set(Student.objects.all()); classes.save() | python manage.py shell_plus
echo from datetime import date; classes=Classes.objects.create(course=Course.objects.get(course_code="ICT123"),enrollment_start_date=date.today(),enrollment_end_date=date.today()); classes.student.set(Student.objects.all()); classes.save() | python manage.py shell_plus
echo from datetime import date; classes=Classes.objects.create(course=Course.objects.get(course_code="DBMS123"),enrollment_start_date=date.today(),enrollment_end_date=date.today()); classes.student.set(Student.objects.all()); classes.save() | python manage.py shell_plus
echo from datetime import date; classes=Classes.objects.create(course=Course.objects.get(course_code="ARB123"),enrollment_start_date=date.today(),enrollment_end_date=date.today()); classes.student.set(Student.objects.all()); classes.save() | python manage.py shell_plus


@REM CREATE 4 ATTENDENCES
echo import datetime; attendence=Attendence.objects.create(date=datetime.date.today(),start_time=datetime.datetime.now(),end_time=datetime.datetime.now(),_class=Classes.objects.get(course=Course.objects.get(course_code="PF123")),status=Attendence.Status.PRESENT); attendence.student.set(Student.objects.all()); attendence.save() | python manage.py shell_plus
echo import datetime; attendence=Attendence.objects.create(date=datetime.date.today(),start_time=datetime.datetime.now(),end_time=datetime.datetime.now(),_class=Classes.objects.get(course=Course.objects.get(course_code="ICT123")),status=Attendence.Status.PRESENT); attendence.student.set(Student.objects.all()); attendence.save() | python manage.py shell_plus
echo import datetime; attendence=Attendence.objects.create(date=datetime.date.today(),start_time=datetime.datetime.now(),end_time=datetime.datetime.now(),_class=Classes.objects.get(course=Course.objects.get(course_code="DBMS123")),status=Attendence.Status.PRESENT); attendence.student.set(Student.objects.all()); attendence.save() | python manage.py shell_plus
echo import datetime; attendence=Attendence.objects.create(date=datetime.date.today(),start_time=datetime.datetime.now(),end_time=datetime.datetime.now(),_class=Classes.objects.get(course=Course.objects.get(course_code="ARB123")),status=Attendence.Status.PRESENT); attendence.student.set(Student.objects.all()); attendence.save() | python manage.py shell_plus


@REM CREATE 4 TimeTables
@REM echo import datetime; TimeTable.objects.create(days=TimeTable.DAYS.MONDAY,start_time=datetime.datetime.now(),end_time=datetime.datetime.now(),room_no=TimeTable.ROOM_NO.ROOM_1,_class=Classes.objects.get(course=Course.objects.get(course_code="PF123"))) | python manage.py shell_plus
@REM echo import datetime; TimeTable.objects.create(days=TimeTable.DAYS.MONDAY,start_time=datetime.datetime.now(),end_time=datetime.datetime.now(),room_no=TimeTable.ROOM_NO.ROOM_1,_class=Classes.objects.get(course=Course.objects.get(course_code="ICT123"))) | python manage.py shell_plus
@REM echo import datetime; TimeTable.objects.create(days=TimeTable.DAYS.MONDAY,start_time=datetime.datetime.now(),end_time=datetime.datetime.now(),room_no=TimeTable.ROOM_NO.ROOM_1,_class=Classes.objects.get(course=Course.objects.get(course_code="DBMS123"))) | python manage.py shell_plus
@REM echo import datetime; TimeTable.objects.create(days=TimeTable.DAYS.MONDAY,start_time=datetime.datetime.now(),end_time=datetime.datetime.now(),room_no=TimeTable.ROOM_NO.ROOM_1,_class=Classes.objects.get(course=Course.objects.get(course_code="ARB123"))) | python manage.py shell_plus

@REM RUN SERVER
python manage.py runserver
