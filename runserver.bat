@REM DJANGO_SETTINGS_MODULE=school.settings
@REM 0<0# : ^
@REM ''' 
@REM @echo off
@REM python %~f0 %* 
@REM exit /b 0
@REM '''

@REM from classes.models import Classes
@REM classes=Classes.objects.create(course=Course.objects.get(course_code="ICT123"),enrollment_start_date=date.today(),enrollment_end_date=date.today()) 
@REM classes.student.set(Student.objects.all())
@REM classes.save()

@REM exit()


@REM echo x="Ahzam Ahmed"; print(x) | python manage.py shell_plus

echo from datetime import date; classes=Classes.objects.create(course=Course.objects.get(course_code="DBMS123"),enrollment_start_date=date.today(),enrollment_end_date=date.today()); classes.student.set(Student.objects.all()); classes.save() | python manage.py shell_plus
