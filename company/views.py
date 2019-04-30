from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

from company.models import Vacancy
from company.serializers import VacancySerializer
from rest_framework import generics


class VacancyList(generics.ListCreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer


class VacancyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer

class ApplyForVacancy(APIView):
    def post(self, request, vacancy_id=None):
        try:
            uid = request.data["uid"]
            answers = request.data["answers"]
        except KeyError:
            return Response({"error": "Must have one correct answer"}, status=status.HTTP_400_BAD_REQUEST)

        for answer in answers:
            pass