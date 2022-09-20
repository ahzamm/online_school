# echo "User.objects.create_superuser(email='superuser@test.com',name='ahzam',password='1234')" | python3 manage.py shell_plus
# echo "course1=Course.objects.create(name='Test Course 1',course_code='TC123 1',ch=Course.CH.FOUR); course1.save()" | python3 manage.py shell_plus
# echo "course2=Course.objects.create(name='Test Course 2',course_code='TC123 2',ch=Course.CH.FOUR); course2.save()" | python3 manage.py shell_plus
# echo "course3=Course.objects.create(name='Test Course 3',course_code='TC123 3',ch=Course.CH.FOUR); course3.save()" | python3 manage.py shell_plus
# echo "course4=Course.objects.create(name='Test Course 4',course_code='TC123 4',ch=Course.CH.FOUR); course4.save()" | python3 manage.py shell_plus

echo "course1=Course.objects.create(name='Test Course 1',course_code='TC123 1',ch=Course.CH.FOUR); course1.save(); course2=Course.objects.create(name='Test Course 2',course_code='TC123 2',ch=Course.CH.FOUR); course2.save(); course3=Course.objects.create(name='Test Course 3',course_code='TC123 3',ch=Course.CH.FOUR); course3.save(); course4=Course.objects.create(name='Test Course 4',course_code='TC123 4',ch=Course.CH.FOUR); course4.save(); course5=Course.objects.create(name='Test Course 5',course_code='TC123 5',ch=Course.CH.FOUR); course5.save(); course = Course.objects.create(name='Test Course 101',course_code='TC123 101',ch=Course.CH.FOUR); course.pre_req_courses.add(course1, course2, course3, course4, course5); course.save()" | python3 manage.py shell_plus

