python manage.py makemigrations classes
python manage.py makemigrations accounts
python manage.py migrate


echo User.objects.create_superuser(email='superuser@test.com',name='ahzam',password='1234') | python manage.py shell_plus


echo Admin.objects.create_user(email="admin1@test.com", name="Admin1", password="1234") | python manage.py shell_plus
echo Admin.objects.create_user(email="admin2@test.com", name="Admin2", password="1234") | python manage.py shell_plus
echo Admin.objects.create_user(email="admin3@test.com", name="Admin3", password="1234") | python manage.py shell_plus


echo Teacher.objects.create_user(email="teacher1@test.com", name="Teacher1", password="1234") | python manage.py shell_plus
echo Teacher.objects.create_user(email="teacher2@test.com", name="Teacher3", password="1234") | python manage.py shell_plus
echo Teacher.objects.create_user(email="teacher3@test.com", name="Teacher3", password="1234") | python manage.py shell_plus


echo Teacher.objects.create_user(email="student1@test.com", name="Student1", password="1234") | python manage.py shell_plus
echo Teacher.objects.create_user(email="student2@test.com", name="Student2", password="1234") | python manage.py shell_plus
echo Teacher.objects.create_user(email="student3@test.com", name="Student3", password="1234") | python manage.py shell_plus


echo Course.objects.create(name="Programming Fundamental",course_code="PF123",teacher=Teacher.objects.get(name="Teacher1"),ch=Course.CH.FOUR) | python manage.py shell_plus
echo Course.objects.create(name="Information and Communication Technology",course_code="ICT123",teacher=Teacher.objects.get(name="Teacher2"),ch=Course.CH.FOUR) | python manage.py shell_plus
echo Course.objects.create(name="Data Base Management System",course_code="DBMS123",teacher=Teacher.objects.get(name="Teacher1"),ch=Course.CH.FOUR) | python manage.py shell_plus
echo Course.objects.create(name="Arabic",course_code="ARB123",teacher=Teacher.objects.get(name="Teacher3"),ch=Course.CH.FOUR) | python manage.py shell_plus


python manage.py runserver
