# Generated by Django 4.0.6 on 2022-09-09 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0003_attendence_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendence',
            name='status',
            field=models.CharField(choices=[('P', 'Present'), ('A', 'Absent')], default='A', max_length=5),
        ),
    ]