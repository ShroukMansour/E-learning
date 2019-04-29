from datetime import timedelta

from django.utils import timezone
from quiz.models import QuizInstance, Quiz, Question, SkillType, Answer
from random import sample


class QuizManipulator():
    class WrongQuizId(Exception):
        pass

    class WrongUserId(Exception):
        pass

    class WrongInstanceId(Exception):
        pass

    class InstanceAlreadyMarked(Exception):
        pass

    class AnswerDoesNotMatch(Exception):
        pass

    class InvalidParams(Exception):
        pass

    def generate_quiz_instance(self, user_id, quiz_id):
        try:
            quiz_to_instantiate = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            raise self.WrongQuizId("No quiz has that id.")

        if not user_id:
            raise self.WrongUserId("No user id supplied.")

        try:
            tbr = QuizInstance.objects.get(user=user_id, quiz=quiz_to_instantiate)
            self.reset_quiz_instance(tbr)
        except QuizInstance.DoesNotExist:
            tbr = self.generate_new_quiz_instance(user_id, quiz_to_instantiate)

        return tbr

    def generate_new_quiz_instance(self, userId, quiz):
        quiz_skill_type = SkillType.objects.get(name=quiz.skill_type)
        tbr = QuizInstance(user=userId, quiz=quiz)
        tbr.save()

        questions = self.generate_quiz_instance_questions(quiz_skill_type, quiz.num_of_questions)
        tbr.questions.add(*questions)
        return tbr

    def reset_quiz_instance(self, quiz_instance):
        quiz_instance.start_time = timezone.now()
        quiz_instance.marked = False
        quiz_instance.finish_time = None
        quiz_instance.score = None
        quiz_instance.passed = False

        quiz = quiz_instance.quiz
        questions = self.generate_quiz_instance_questions(quiz.skill_type, quiz.num_of_questions)
        quiz_instance.questions.clear()
        quiz_instance.questions.add(*questions)

        quiz_instance.save()

    def generate_quiz_instance_questions(self, quiz_skill_type, num_of_questions):
        quiz_questions = Question.objects.filter(skill_type=quiz_skill_type.pk)
        quiz_questions_set = set(quiz_question for quiz_question in quiz_questions)
        return sample(quiz_questions_set, k=num_of_questions)

    def instance_exists(self, user_id, quiz_id):
        temp = QuizInstance.objects.filter(user=user_id).filter(quiz=quiz_id)

        return len(temp) == 1

    def evaluate_quiz_instance(self, quiz_instance_id, answers):
        try:
            quiz_instance = QuizInstance.objects.get(id=quiz_instance_id)
        except QuizInstance.DoesNotExist:
            raise self.WrongInstanceId

        if quiz_instance.marked:
            raise self.InstanceAlreadyMarked

        quiz_instance.finish_time = timezone.now()

        score = 0
        try:
            for answer in answers:
                atemp = Answer.objects.get(id=answer['aid'])

                if atemp.question.id != answer['qid']:
                    raise self.AnswerDoesNotMatch

                if atemp.is_correct:
                    score += 1

        except (Answer.DoesNotExist, KeyError):
            raise self.InvalidParams

        expected_finish_time = quiz_instance.start_time + timedelta(minutes=quiz_instance.quiz.expected_duration)

        quiz_instance.marked = True
        quiz_instance.score = score
        quiz_instance.passed = \
            (score >= quiz_instance.quiz.pass_score and \
             quiz_instance.finish_time <= expected_finish_time)
        quiz_instance.save()

        return {
            "score": score,
            "passed": quiz_instance.passed
        }
