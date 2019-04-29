from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

from datetime import timedelta

from .models import Question, Quiz, QuizInstance, SkillType, Answer
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
            return Response({"error": "Must have one correct answer"}, status=status.HTTP_400_BAD_REQUEST)

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

        return queryset


class SkillTypeViewSet(viewsets.ModelViewSet):
    queryset = SkillType.objects.all()
    serializer_class = SkillTypeSerializer


class TakeQuiz(APIView):
    quiz_manipulator = QuizManipulator()

    def post(self, request, quiz_id):
        try:
            tbr = self.quiz_manipulator.generate_quiz_instance(self.request.data['uid'], quiz_id)

        except (QuizManipulator.WrongQuizId, QuizManipulator.WrongUserId):
            return Response({"error": "Invalid Arguments."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = QuizInstanceSerializer(tbr)
        return Response(serializer.data)

class SubmitQuiz(APIView):
    def post(self, request, instance_id):
        try:
            tbr = self.quiz_manipulator.evaluate_quiz_instance(instance_id, request.data['answers'])

        except InstanceAlreadyMarked:
            return Response({"error": "Instance Already Marked."}, status=status.HTTP_400_BAD_REQUEST)
        except (AnswerDoesNotMatch, InvalidParams):
            return Response({"error": "Invalid Arguments."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(tbr)

class SkillScore(APIView):
    def get(self, request, skill_type_id=None):
        uid = self.request.query_params.get('uid')
        if not uid:
            return Response({"error": "No user id supplied."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            stemp = SkillType.objects.get(id=skill_type_id)
        except SkillType.DoesNotExist:
            return Response({"error": "Invalid skill type id."}, status=status.HTTP_400_BAD_REQUEST)

        quizzes_taken = QuizInstance.objects.filter(user=uid, quiz__skill_type=stemp)
        score = 0
        for quiz in quizzes_taken:
            if quiz.marked and quiz.passed:
                score += quiz.score

        return Response({"score": score})