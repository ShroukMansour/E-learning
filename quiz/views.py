from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

from datetime import timedelta

from .models import Question, Quiz, QuizInstance, SkillType, Answer, APILog
from .serializers import QuestionSerializer, QuizSerializer, QuizInstanceSerializer, SkillTypeSerializer

from quiz.Classes.QuizManipulator import QuizManipulator


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def create(self, request, **kwargs):
        correct_answers = 0
        answers = request.data['answers']
        for answer in answers:
            if 'is_correct' in answer and answer["is_correct"]:
                correct_answers = correct_answers + 1
        if correct_answers != 1:
            log = APILog(description="Admin tried to create new question but didn't send correct answer.")
            log.save()
            return Response({"error": "Must have one correct answer"}, status=status.HTTP_400_BAD_REQUEST)

        log = APILog(description="Admin created a new question.")
        log.save()
        return super(QuestionViewSet, self).create(request, kwargs)


class QuizViewSet(viewsets.ModelViewSet):
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()

    def get_queryset(self):
        skill_type = self.request.query_params.getlist('skillType')

        if skill_type:
            skill_type = SkillType.objects.filter(name__in=skill_type)
            queryset = Quiz.objects.filter(skill_type__in=skill_type)
        else:
            queryset = Quiz.objects.all()

        desc = "User searched for Quizzes with skill types: "
        for skill in self.request.query_params.getlist('skillType'):
            desc += skill + ", "

        log = APILog(description=desc)
        log.save()
        return queryset

    def create(self, request, **kwargs):
        if request.data['pass_score'] > request.data['num_of_questions']:
            log = APILog(description="Admin tried to create new quiz but sent invalid pass score.")
            log.save()
            return Response({"error": "Pass score can't be greater than number of questions "}, status=status.HTTP_400_BAD_REQUEST)
        
        if not self.validate_num_questions(request.data):
            log = APILog(description="Admin tried to create new quiz but sent invalid number of questions.")
            log.save()
            return Response({"error": "No enough questions in this skill"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        log = APILog(description="Admin created new quiz.")
        log.save()
        return super(QuizViewSet, self).create(request, kwargs)

    def validate_num_questions(self, data):
        skill_type_filter = SkillType.objects.filter(**data["skill_type"])
        if not skill_type_filter.exists():
            return False
        skill_type_filter = SkillType.objects.get(**data["skill_type"])
        questions_set = Question.objects.filter(skill_type=skill_type_filter)
        if len(questions_set) < data['num_of_questions']:
            return False
        return True

class SkillTypeViewSet(viewsets.ModelViewSet):
    queryset = SkillType.objects.all()
    serializer_class = SkillTypeSerializer


class TakeQuiz(APIView):
    quiz_manipulator = QuizManipulator()

    def post(self, request, quiz_id):
        try:
            tbr = self.quiz_manipulator.generate_quiz_instance(request.data['uid'], quiz_id)

        except (QuizManipulator.WrongQuizId, QuizManipulator.WrongUserId):
            log = APILog(description="User tried to take a quiz but sent invaid parameters.")
            log.save()
            return Response({"error": "Invalid Arguments."}, status=status.HTTP_400_BAD_REQUEST)


        log = APILog(description="User with id " + str(request.data['uid']) + " took the quiz with id " + str(quiz_id) + ".")
        log.save()
        serializer = QuizInstanceSerializer(tbr)
        return Response(serializer.data)


class SubmitQuiz(APIView):
    quiz_manipulator = QuizManipulator()

    def post(self, request, quiz_instance_id):
        try:
            tbr = self.quiz_manipulator.evaluate_quiz_instance(quiz_instance_id, request.data['answers'])

        except QuizManipulator.InstanceAlreadyMarked:
            log = APILog(description="User tried to submit quiz instance with id " + str(quiz_instance_id) + " but it's already marked.")
            log.save()
            return Response({"error": "Instance Already Marked."}, status=status.HTTP_400_BAD_REQUEST)

        except (QuizManipulator.AnswerDoesNotMatch, QuizManipulator.InvalidParams, QuizManipulator.WrongInstanceId):
            log = APILog(description="User tried to submit quiz instance with id " + str(quiz_instance_id) + " but sent invalid parameters.")
            log.save()
            return Response({"error": "Invalid Arguments."}, status=status.HTTP_400_BAD_REQUEST)

        log = APILog(description="User tried to submit quiz instance with id " + str(quiz_instance_id) + " but sent invalid parameters.")
        log.save()
        return Response(tbr)


class SkillScore(APIView):
    def get(self, request, skill_type_id=None):
        uid = request.query_params.get('uid')
        if not uid:
            log = APILog(description="User searched for his score but didn't send his id.")
            log.save()
            return Response({"error": "No user id supplied."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            stemp = SkillType.objects.get(id=skill_type_id)
        except SkillType.DoesNotExist:
            log = APILog(description="User searched for his score but sent invalid skill type.")
            log.save()
            return Response({"error": "Invalid skill type id."}, status=status.HTTP_400_BAD_REQUEST)

        quizzes_taken = QuizInstance.objects.filter(user=uid, quiz__skill_type=stemp)
        score = 0
        for quiz in quizzes_taken:
            if quiz.marked and quiz.passed:
                score += quiz.score

        log = APILog(description="User with id " + str(uid) + " searched for his score in skill type " + stemp.name + ".")
        log.save()
        return Response({"score": score})
