import json
from django.db import IntegrityError, transaction
from rest_framework import status
from rest_framework.test import APITestCase

from company.models import Vacancy, VacancyQuestion, Choice, JobType
from quiz.models import SkillType


class PostVacancyTest(APITestCase):
    def setUp(self):
        JobType.objects.create(name='Full Time')
        JobType.objects.create(name='Half Time')
        JobType.objects.create(name='Intern')
        self.data = {"company_id": 1,
                     "title": "Software Engineer",
                     "description": "Design programs",
                     "requirements": "problem solving skills",
                     "benefits": "transportation covered",
                     "salary": 2000,
                     "job_type": "Full Time",
                     "interest_field": {
                         "name": "java"
                     },
                     "vacancy_questions": [
                         {
                             "question_text": "How old are you",
                             "question_choices": [
                                 {
                                     "choice_text": "20"
                                 },
                                 {
                                     "choice_text": "30"
                                 }
                             ]
                         }
                     ]
                     }

    def test_post_valid_vacancy(self):
        SkillType.objects.create(name='java')
        url = '/vacancies/'
        response = self.client.post(url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vacancy.objects.count(), 1)
        self.assertEqual(VacancyQuestion.objects.count(), 1)
        self.assertEqual(Choice.objects.count(), 2)
        self.assertEqual(SkillType.objects.count(), 1)
        self.assertEqual(Vacancy.objects.get().title, "Software Engineer")

    def test_post_vacancy_with_non_existent_interest(self):
        url = '/vacancies/'
        response = self.client.post(url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vacancy.objects.count(), 1)
        self.assertEqual(VacancyQuestion.objects.count(), 1)
        self.assertEqual(Choice.objects.count(), 2)
        self.assertEqual(SkillType.objects.count(), 1)
        self.assertEqual(Vacancy.objects.get().title, "Software Engineer")

    def test_post_vacancy_with_invalid_job_type(self):
        url = '/vacancies/'
        self.data['job_type'] = "invalid"
        response = self.client.post(url, data=self.data, format='json')
        self.data['job_type'] = "Full Time"
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_vacancy_with_same_choices_for_different_questions(self):
        url = '/vacancies/'
        # self.data['vacancy_questions'][0]['question_choices'][1]['choice_text'] = "20"
        response1 = self.client.post(url, data=self.data, format='json')
        response2 = self.client.post(url, data=self.data, format='json')
        # self.data['job_type'] = "Full Time"
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vacancy.objects.count(), 2)
        self.assertEqual(VacancyQuestion.objects.count(), 2)
        self.assertEqual(Choice.objects.count(), 4)
        self.assertEqual(SkillType.objects.count(), 1)

    def test_vacancy_with_same_choices_in_same_question(self):
        url = '/vacancies/'
        self.data['vacancy_questions'][0]['question_choices'][1]['choice_text'] = "20"
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.client.post(url, data=self.data, format='json')
        self.data['vacancy_questions'][0]['question_choices'][1]['choice_text'] = "30"
        self.assertEqual(Vacancy.objects.count(), 0)
        self.assertEqual(VacancyQuestion.objects.count(), 0)
        self.assertEqual(Choice.objects.count(), 0)
        self.assertEqual(SkillType.objects.count(), 0)


class GetVacancyTest(APITestCase):
    def create_vacancy(self, title):
        self.data = {"company_id": 1,
                     "title": title,
                     "description": "Design programs",
                     "requirements": "problem solving skills",
                     "benefits": "transportation covered",
                     "salary": 2000,
                     "job_type": "Full Time",
                     "interest_field": {
                         "name": "java"
                     },
                     "vacancy_questions": [
                         {
                             "question_text": "How old are you",
                             "question_choices": [
                                 {
                                     "choice_text": "20"
                                 },
                                 {
                                     "choice_text": "30"
                                 }
                             ]
                         }
                     ]
                     }
        url = '/vacancies/'
        response = self.client.post(url, data=self.data, format='json')

    def setUp(self):
        JobType.objects.create(name='Full Time')
        JobType.objects.create(name='Half Time')
        JobType.objects.create(name='Intern')
        self.create_vacancy("software engineer")
        self.create_vacancy("software architect")

    def test_get_all_quizzes_successfully(self):
        url = '/vacancies/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_quiz_by_id(self):
        data = {"company_id": 1,
                "title": "software architect",
                "description": "Design programs",
                "requirements": "problem solving skills",
                "benefits": "transportation covered",
                "salary": 2000,
                "job_type": "Full Time",
                "interest_field": {
                    "id": 1,
                    "name": "java"
                },
                "vacancy_questions": [
                    {
                        "question_text": "How old are you",
                        "question_choices": [
                            {
                                "choice_text": "20"
                            },
                            {
                                "choice_text": "30"
                            }
                        ]
                    }
                ]
                }
        url = '/vacancies/2/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = json.loads(response.content)
        json_response.pop('id')
        self.assertEqual(json_response, data)

    def test_get_non_existent_quiz(self):
        url = '/vacancies/10/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
