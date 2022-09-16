# echo "User.objects.create_superuser(email='superuser@test.com',name='ahzam',password='1234')" | python3 manage.py shell_plus

echo "import datetime; attendence=Attendence.objects.create(date=datetime.date.today(),start_time=datetime.datetime.now(),end_time=datetime.datetime.now(),_class=Classes.objects.get(course=Course.objects.get(course_code='PF123')),status=Attendence.Status.PRESENT); attendence.student.set(Student.objects.all()); attendence.save()" | python3 manage.py shell_plus
