from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

from company.models import Vacancy, VacancyApplication, VacancyAnswer, VacancyQuestion, APILog
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
            log = APILog(description=("User Searched for Vacancies in company with id " + str(companyId)))
        else:
            queryset = Vacancy.objects.all()
            log = APILog(description="User Searched for all Vacancies")

        log.save()
        return queryset


class VacancyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer

    def get_queryset(self):
        log = APILog(description="User Searched for Vacancy with id " + str(self.kwargs.get('pk')))
        log.save()
        
        return Vacancy.objects.filter(id=self.kwargs.get('pk'))


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
        except (KeyError, VacancyQuestion.DoesNotExist):
            for db_object in db_objects:
                db_object.delete()

            log = APILog(description=("User with id " + str(uid) + " applied for Vacancy with id " + str(app.id) + "but send invalid parameters."))
            log.save()
            return Response({"error": "Invalid Params."}, status=status.HTTP_400_BAD_REQUEST)

        log = APILog(description=("User with id " + str(uid) + " applied for Vacancy with id " + str(app.id)))
        log.save()
        return Response()


class VacancyApplicationList(APIView):
    def get(self, request):
        try:
            vacany_id = request.query_params.get('vacancyId')

            if vacany_id:
                applications = VacancyApplication.objects.filter(vacancy=Vacancy.objects.get(id=vacany_id))
            else:
                applications = VacancyApplication.objects.none()

            tbr = []
            for app in applications:
                answers = VacancyAnswer.objects.filter(vacancy_application=app)
                tbr.append({
                    "application": VacancyApplicationSerializer(app).data,
                    "answers": VacancyAnswerSerializer(answers, many=True).data
                })
            
            log = APILog(description=("User with id " + str(uid) + " applied for Vacancy with id " + str(app.id)))
            log.save()

            return Response(tbr)
        except:
            log = APILog(description=("User with id " + str(uid) + " applied for Vacancy with id " + str(app.id) + "but send invalid parameters."))
            log.save()
            return Response({"error": "Invalid Params."}, status=status.HTTP_400_BAD_REQUEST)
