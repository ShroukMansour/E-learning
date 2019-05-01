from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

from company.models import Vacancy, VacancyApplication, VacancyAnswer, VacancyQuestion
from company.serializers import VacancySerializer, VacancyApplicationSerializer, VacancyAnswerSerializer
from rest_framework import generics


class VacancyList(generics.ListCreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer

    def get_queryset(self):
        companyId = self.request.query_params.getlist('companyId')
        companyId = [s for s in companyId if s.isdigit()]

        if companyId:
            queryset = Vacancy.objects.filter(company_id__in=companyId)
        else:
            queryset = Vacancy.objects.all()

        return queryset


class VacancyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer


class ApplyForVacancy(APIView):
    def post(self, request, vacancy_id=None):
        db_objects = []
        try:
            uid = request.data["uid"]
            answers = request.data["answers"]

            app = VacancyApplication(user_id=uid, vacancy=Vacancy.objects.get(id=vacancy_id))
            db_objects.append(app)
            app.save()

            for answer in answers:
                question = VacancyQuestion.objects.get(id=answer["questionId"])
                answer = VacancyAnswer(\
                    question=question,\
                    answer_text=answer["answer"],\
                    vacancy_application=app\
                )

                db_objects.append(answer)
                answer.save()
        except (KeyError, VacancyQuestion.DoesNotExist, VacancyQuestion.DoesNotExist):
            for db_object in db_objects:
                db_object.delete()

            return Response({"error": "Invalid Params."}, status=status.HTTP_400_BAD_REQUEST)

        return Response()


class VacancyApplicationList(APIView):
    def get(self, request):
        try:
            vacany_id = self.request.query_params.get('vacanyId')

            if vacany_id:
                applications = VacancyApplication.objects.filter(vacancy=Vacancy.objects.get(id=vacany_id))
            else:
                applications = VacancyApplication.objects.none()

            tbr = {"apps": []}
            for app in applications:
                answers = VacancyAnswer.objects.filter(vacancy_application=app)
                tbr["apps"].append({
                    "application": VacancyApplicationSerializer(app).data,
                    "answers": VacancyAnswerSerializer(answers, many=True).data
                })
            
            return Response(tbr)
        except:
            return Response({"error": "Invalid Params."}, status=status.HTTP_400_BAD_REQUEST)
