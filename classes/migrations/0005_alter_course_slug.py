# Generated by Django 4.0.3 on 2022-09-24 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classes", "0004_alter_course_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="slug",
            field=models.SlugField(blank=True, max_length=100, unique=True),
        ),
    ]
