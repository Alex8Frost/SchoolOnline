from django.shortcuts import render
from .models import *
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


class StudentsViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):

    serializer_class = StudentsSerializer

    def get_queryset(self):
        return Students.objects.all()

    def list(self, request, *args, **kwargs):
         serializer = self.serializer_class(self.get_queryset(), many=True)
         return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductsViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):

    serializer_class = ProductsSerializer

    def get_queryset(self):
        return Products.objects.all()

    def list(self, request, *args, **kwargs):
         serializer = self.serializer_class(self.get_queryset(), many=True)
         return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class GroupsViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):

    serializer_class = GroupsSerializer

    def get_queryset(self):
        return Groups.objects.all()

    def list(self, request, *args, **kwargs):
         serializer = self.serializer_class(self.get_queryset(), many=True)
         return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class LessonsViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):

    serializer_class = LessonsSerializer

    def get_queryset(self):
        return Lessons.objects.all()

    def list(self, request, *args, **kwargs):
         serializer = self.serializer_class(self.get_queryset(), many=True)
         return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)






