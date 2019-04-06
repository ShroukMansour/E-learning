from django.test import TestCase

from company.models import Vacancy, VacancyQuestion, Choice
from company.serializers import VacancyQuestionSerializer, VacancySerializer


class test(TestCase):

    def test_serializers(self):
        self.create_data()
        v = Vacancy.objects.get(id=1)
        q = VacancyQuestion.objects.get(id=1)
        c = Choice.objects.get(choice_text="five")
        ser = VacancySerializer(v)
        print(ser.data)
        ser = VacancyQuestionSerializer(q)
        print(ser.data)

    def create_data(self):
        v = Vacancy.objects.create(company_id=1, title="hjfd", description="kfjg", requirements="kfgjfkj", benefits="kfjdkg", salary=1111, job_type="Full Time", interest_field="kjgdfkj")
        q = VacancyQuestion.objects.create(question_text="How old are you?", vacancy=v)
        c = Choice.objects.create(choice_text="five", question=q)
