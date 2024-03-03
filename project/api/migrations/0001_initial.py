# Generated by Django 4.2.3 on 2024-03-01 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher', models.CharField(max_length=32, verbose_name='Создатель')),
                ('name_product', models.CharField(max_length=32, verbose_name='Название продукта')),
                ('date_time_start', models.DateTimeField(verbose_name='Дата и время старта')),
                ('coast', models.PositiveBigIntegerField(verbose_name='Стоимость')),
                ('min_students_group', models.PositiveIntegerField(verbose_name='Минимальное кол-во студентов в группе')),
                ('max_students_group', models.PositiveIntegerField(verbose_name='Максимальное кол-во студентов в группе')),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_student', models.CharField(max_length=32, verbose_name='Имя студента')),
                ('product_id', models.ManyToManyField(related_name='student_id', to='api.products', verbose_name='Продукт')),
            ],
        ),
        migrations.CreateModel(
            name='Lessons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_lesson', models.CharField(max_length=32, verbose_name='Название урока')),
                ('video_link', models.URLField(verbose_name='Ссылка на видео')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.products', verbose_name='Название продукта')),
            ],
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_group', models.CharField(max_length=32, verbose_name='Название группы')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.products', verbose_name='Название продукта')),
                ('student_id', models.ManyToManyField(related_name='group_id', to='api.students', verbose_name='Студент')),
            ],
        ),
    ]
