python manage.py makemigrations classes
python manage.py migrate
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('ahzam', 'ahzam@test.com', '1234')" | python manage.py shell
python manage.py runserver
