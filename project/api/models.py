from django.db import models


class Products(models.Model):

    teacher = models.CharField(max_length=32, verbose_name='Создатель')
    name_product = models.CharField(max_length=32, verbose_name='Название продукта')
    date_time_start = models.DateTimeField(verbose_name='Дата и время старта')
    coast = models.PositiveBigIntegerField(verbose_name='Стоимость')
    min_students_group = models.PositiveIntegerField(verbose_name='Минимальное кол-во студентов в группе')
    max_students_group = models.PositiveIntegerField(verbose_name='Максимальное кол-во студентов в группе')


class Students(models.Model):

    name_student = models.CharField(max_length=32, verbose_name='Имя студента')
    product_id = models.ManyToManyField(Products, related_name='student_id', verbose_name='Продукт')


class Groups(models.Model):

    name_group = models.CharField(max_length=32, verbose_name='Название группы')
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Название продукта')
    student_id = models.ManyToManyField(Students, related_name='group_id', verbose_name='Студент')


class Lessons(models.Model):

    name_lesson = models.CharField(max_length=32, verbose_name='Название урока')
    video_link = models.URLField(verbose_name='Ссылка на видео')
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Название продукта')