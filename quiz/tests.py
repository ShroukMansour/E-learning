import json

from rest_framework.test import APITestCase
from rest_framework import status
from quiz.models import Question, SkillType, Answer, Quiz


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
        self.assertEqual(Answer.objects.count(), 3)
        self.assertEqual(SkillType.objects.count(), 1)
        self.assertEqual(Answer.objects.get(answer_text="public").is_correct, True)
        self.assertEqual(Question.objects.get().question_text, "what are the most famous type of inheritance?")

    def test_post_question_with_new_skill(self):
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
        self.assertEqual(Answer.objects.count(), 3)
        self.assertEqual(SkillType.objects.count(), 1)
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

    def test_post_question_without_answers(self):
        SkillType.objects.create(name='java')
        url = '/questions/'
        data = {'question_text': "what are the most famous type of inheritance?",
                'question_type': 'MCQ',
                'score': 1,
                'skill_type': {"name": "java"},
                'answers': []
                }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_question_with_req_parameters_only(self):
        SkillType.objects.create(name='java')
        url = '/questions/'
        data = {'question_text': "what are the most famous type of inheritance?",
                'skill_type': {"name": "java"},
                'answers': [{"answer_text": 'public', "is_correct": True},
                            {"answer_text": 'public'},
                            {"answer_text": 'protected'}]
                }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Answer.objects.count(), 3)
        self.assertEqual(SkillType.objects.count(), 1)
        self.assertEqual(Question.objects.get().question_type, "MCQ")
        self.assertEqual(Question.objects.get().score, 1)

    def test_post_question_with_same_choices_names(self):
        SkillType.objects.create(name='java')
        url = '/questions/'
        data = {'question_text': "what are the most famous type of inheritance?",
                'question_type': 'MCQ',
                'score': 1,
                'skill_type': {"name": "java"},
                'answers': [{"answer_text": 'public', "is_correct": True},
                            {"answer_text": 'public'},
                            {"answer_text": 'protected'}]
                }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Answer.objects.count(), 3)
        self.assertEqual(SkillType.objects.count(), 1)
        self.assertEqual(Question.objects.get().question_text, "what are the most famous type of inheritance?")


class PostQuizTest(APITestCase):
    def create_question(self, title):
        url = '/questions/'
        data = {'question_text': title,
                'question_type': 'MCQ',
                'score': 1,
                'skill_type': {"id": 1, "name": "java"},
                'answers': [{"answer_text": 'public', "is_correct": True},
                            {"answer_text": 'private'},
                            {"answer_text": 'protected'}]
                }
        self.client.post(url, data=data, format='json')

    def setUp(self):
        self.create_question("what's the most popular inheritance in java?")
        self.create_question("what's the most popular inheritance in python?")
        self.create_question("what's the most popular inheritance in matlab?")

    def test_post_valid_quiz(self):
        url = '/quizzes/'
        data = {'title': "superheroes java",
                'pass_score': 1,
                'num_of_questions': 3,
                'expected_duration': 10,
                'skill_type': {"name": "java"},
                }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quiz.objects.count(), 1)
        self.assertEqual(SkillType.objects.count(), 1)
        self.assertEqual(Quiz.objects.get().title, "superheroes java")

    def test_post_quiz_with_invalid_questions_num(self):
        url = '/quizzes/'
        data = {'title': "superheroes java",
                'pass_score': 1,
                'num_of_questions': 5,
                'expected_duration': 10,
                'skill_type': {"name": "java"},
                }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_quiz_with_invalid_pass_score(self):
        url = '/quizzes/'
        data = {'title': "superheroes java",
                'pass_score': 5,
                'num_of_questions': 3,
                'expected_duration': 10,
                'skill_type': {"name": "java"},
                }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetQuizTest(APITestCase):
    def create_question(self, title, skill):
        url = '/questions/'
        data = {'question_text': title,
                'question_type': 'MCQ',
                'score': 1,
                'skill_type': {"name": skill},
                'answers': [{"answer_text": 'public', "is_correct": True},
                            {"answer_text": 'private'},
                            {"answer_text": 'protected'}]
                }
        self.client.post(url, data=data, format='json')

    def create_quiz(self, title, skill):
        url = '/quizzes/'
        data = {'title': title,
                'pass_score': 2,
                'num_of_questions': 3,
                'expected_duration': 10,
                'skill_type': {"name": skill},
                }
        response = self.client.post(url, data=data, format='json')

    def setUp(self):
        self.create_question("what's the most popular inheritance in java?", "java")
        self.create_question("what's the most popular inheritance in python?", "java")
        self.create_question("what's the most popular inheritance in matlab?", "java")
        self.create_question("what's the most popular inheritance in java?", "python")
        self.create_question("what's the most popular inheritance in python?", "python")
        self.create_question("what's the most popular inheritance in matlab?", "python")
        self.create_quiz("superheroes quiz", "java")
        self.create_quiz("welcome quiz", "java")

    def test_get_all_quizzes_successfully(self):
        url = '/quizzes/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_quiz_by_id(self):
        url = '/quizzes/1/'
        data = {'title': "superheroes quiz",
                'pass_score': 2,
                'num_of_questions': 3,
                'expected_duration': 10,
                'skill_type': {"id": 1, "name": "java"},
                }
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = json.loads(response.content)
        json_response.pop('id')
        self.assertEqual(json_response, data)

    def test_get_non_existent_quiz(self):
        url = '/quizzes/10/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_quiz_successfully_by_skill(self):
        url = '/quizzes/'
        response = self.client.get(url, data={"skillType": "java"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_quiz_by_nonexistent_skill(self):
        url = '/quizzes/'
        response = self.client.get(url, data={"skillType": "python"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_quiz_by_skill_list(self):
        self.create_question("python question", "python")
        self.create_quiz("python quiz", "python")
        url = '/quizzes/'
        response = self.client.get(url, data={"skillType": ["python", "java"]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_quiz_by_skill_list_2(self):
        self.create_question("python question", "python")
        self.create_quiz("python quiz", "python")
        url = '/quizzes/'
        response = self.client.get(url, data={"skillType": ["python", "matlab"]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class TakeQuizTest(APITestCase):
    def create_question(self, title, skill):
        url = '/questions/'
        data = {'question_text': title,
                'question_type': 'MCQ',
                'score': 1,
                'skill_type': {"name": skill},
                'answers': [{"answer_text": 'public', "is_correct": True},
                            {"answer_text": 'private'},
                            {"answer_text": 'protected'}]
                }
        self.client.post(url, data=data, format='json')

    def create_quiz(self, title, skill):
        url = '/quizzes/'
        data = {'title': title,
                'pass_score': 2,
                'num_of_questions': 3,
                'expected_duration': 10,
                'skill_type': {"name": skill},
                }
        response = self.client.post(url, data=data, format='json')

    def setUp(self):
        self.create_question("what's the most popular inheritance in java?", "java")
        self.create_question("what's the most popular inheritance in python?", "java")
        self.create_question("what's the most popular inheritance in matlab?", "java")
        self.create_quiz("superheroes quiz", "java")

    def test_take_quiz_successfully(self):
        url = '/quiz/take/1'
        data = {'id': 1,
                'question_text': "what's the most popular inheritance in java?",
                'question_type': 'MCQ',
                'score': 1,
                'skill_type': {"id": 1, "name": "java"},
                'answers': [{'id': 1, "answer_text": 'public'},
                            {'id': 2, "answer_text": 'private'},
                            {'id': 3, "answer_text": 'protected'}]
                }
        response = self.client.post(url, data={'uid': 1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(len(response.data['questions']), 3)
        json_response = json.loads(response.content)
        json_response = json_response['questions'][0]
        self.assertEqual(json_response, data)

    def test_take_quiz_with_invalid_id(self):
        url = '/quiz/take/10'
        response = self.client.post(url, data={'uid': 1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SubmitQuizTest(APITestCase):
    def create_question(self, title, skill):
        url = '/questions/'
        data = {'question_text': title,
                'question_type': 'MCQ',
                'score': 1,
                'skill_type': {"name": skill},
                'answers': [{"answer_text": 'public', "is_correct": True},
                            {"answer_text": 'private'},
                            {"answer_text": 'protected'}]
                }
        self.client.post(url, data=data, format='json')

    def create_quiz(self, title, skill):
        url = '/quizzes/'
        data = {'title': title,
                'pass_score': 3,
                'num_of_questions': 3,
                'expected_duration': 10,
                'skill_type': {"name": skill},
                }
        response = self.client.post(url, data=data, format='json')

    def take_quiz(self):
        url = '/quiz/take/1'
        response = self.client.post(url, data={'uid': 1}, format='json')
        self.quiz_instance = response.data

    def setUp(self):
        self.create_question("what's the most popular inheritance in java?", "java")
        self.create_question("what's the most popular inheritance in python?", "java")
        self.create_question("what's the most popular inheritance in matlab?", "java")
        self.create_quiz("superheroes quiz", "java")
        self.take_quiz()
        self.data = {'answers': [
            {"qid": self.quiz_instance["questions"][0]['id'],
             "aid": self.quiz_instance["questions"][0]['answers'][0]['id']},
            {"qid": self.quiz_instance["questions"][1]['id'],
             "aid": self.quiz_instance["questions"][1]['answers'][0]['id']},
            {"qid": self.quiz_instance["questions"][2]['id'],
             "aid": self.quiz_instance["questions"][2]['answers'][0]['id']}
        ]}

    def test_submit_quiz_successfully(self):
        url = '/quiz/submit/1'

        response = self.client.post(url, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['score'], 3)
        self.assertEqual(response.data['passed'], True)

    def test_submit_quiz_with_invalid_id(self):
        url = '/quiz/submit/10'
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_submit_quiz_with_invalid_answer_question_match(self):
        url = '/quiz/submit/1'
        self.data = {'answers': [
            {"qid": self.quiz_instance["questions"][0]['id'],
             "aid": self.quiz_instance["questions"][0]['answers'][0]['id']},
            {"qid": self.quiz_instance["questions"][1]['id'],
             "aid": self.quiz_instance["questions"][0]['answers'][0]['id']},
            {"qid": self.quiz_instance["questions"][2]['id'],
             "aid": self.quiz_instance["questions"][0]['answers'][0]['id']}
        ]}
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class SkillTypeTest(APITestCase):
    def create_question(self, title, skill):
        url = '/questions/'
        data = {'question_text': title,
                'question_type': 'MCQ',
                'score': 1,
                'skill_type': {"name": skill},
                'answers': [{"answer_text": 'public', "is_correct": True},
                            {"answer_text": 'private'},
                            {"answer_text": 'protected'}]
                }
        self.client.post(url, data=data, format='json')

    def create_quiz(self, title, skill):
        url = '/quizzes/'
        data = {'title': title,
                'pass_score': 3,
                'num_of_questions': 3,
                'expected_duration': 10,
                'skill_type': {"name": skill},
                }
        response = self.client.post(url, data=data, format='json')

    def take_quiz(self):
        url = '/quiz/take/1'
        response = self.client.post(url, data={'uid': 1}, format='json')
        self.quiz_instance = response.data

    def submit_quiz(self):
        url = '/quiz/submit/1'
        data = {'answers': [
            {"qid": self.quiz_instance["questions"][0]['id'],
             "aid": self.quiz_instance["questions"][0]['answers'][0]['id']},
            {"qid": self.quiz_instance["questions"][1]['id'],
             "aid": self.quiz_instance["questions"][1]['answers'][0]['id']},
            {"qid": self.quiz_instance["questions"][2]['id'],
             "aid": self.quiz_instance["questions"][2]['answers'][0]['id']}
        ]}
        response = self.client.post(url, data=data, format='json')

    def setUp(self):
        url = "/skillTypes/"
        response = self.client.post(url, data={"name": "java"}, format = 'json')
        response = self.client.post(url, data={"name": "python"}, format = 'json')
        response = self.client.get(url, format = 'json')
        self.skill_id = response.data[0]['id']
        self.create_question("what's the most popular inheritance in java?", "java")
        self.create_question("what's the most popular inheritance in python?", "java")
        self.create_question("what's the most popular inheritance in matlab?", "java")
        self.create_quiz("superheroes quiz", "java")
        self.take_quiz()

    def test_get_score_for_user(self):
        self.submit_quiz()
        url = "/quiz/score/" + str(self.skill_id)
        response = self.client.get(url, data={"uid": "1"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['score'], 3)

    def test_get_score_for_not_marked_skill(self):
        url = "/quiz/score/" + str(self.skill_id)
        response = self.client.get(url, data={"uid": "1"}, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['score'], 0)


