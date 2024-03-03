from .models import *
from rest_framework import serializers


class StudentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Students
        fields = ('name_student', 'product_id')


class ProductsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = ('teacher', 'name_product', 'date_time_start', 'coast', 'min_students_group', 'max_students_group')


class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = ('name_group', 'product_id', 'student_id')


class LessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = ('name_lesson', 'video_link', 'product_id')