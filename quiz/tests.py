from rest_framework.test import APITestCase
from rest_framework import status
from quiz.models import Question, SkillType


# Create your tests here.
class QuestionTest(APITestCase):
    def test_post_valid_question(self):
        SkillType.objects.create(name='java')
        url = '/questions/'
        data = {'question_text': "what are the most famous type of inheritance?",
                'question_type': 'MCQ',
                'score': 1,
                'skill_type': {"name": "java"},
                'answers': [{"answer_text": 'public', "is_correct": True},
                            {"answer_text": 'private'},
                            {"answer_text": 'protected'}]
                }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Question.objects.get().question_text, "what are the most famous type of inheritance?")

    def test_post_question_with_new_skill(self):
        url = '/questions/'
        data = {'question_text': "what are the most famous type of inheritance",
                'question_type': 'MCQ',
                'score': 1,
                'skill_type': {"name": "java"},
                'answers': [{"answer_text": 'public', "is_correct" : True},
                            {"answer_text": 'private'},
                            {"answer_text": 'protected'}]
                }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Question.objects.get().question_text, "what are the most famous type of inheritance?")


    def test_post_question_with_multiple_correct_answer(self):
        SkillType.objects.create(name='java')
        url = '/questions/'
        data = {'question_text': "what are the most famous type of inheritance?",
                'question_type': 'MCQ',
                'score': 1,
                'skill_type': {"name": "java"},
                'answers': [{"answer_text": 'public', "is_correct": True},
                            {"answer_text": 'private', "is_correct": True},
                            {"answer_text": 'protected'}]
                }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)