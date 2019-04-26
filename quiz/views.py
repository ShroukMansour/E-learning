from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from django.utils import timezone

from random import sample
from datetime import timedelta

from .models import Question, Quiz, QuizInstance, SkillType, Answer
from .serializers import QuestionSerializer, QuizSerializer, QuizInstanceSerializer, SkillTypeSerializer


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


class QuizInstances(APIView):

    def get(self, request, id=None):
        try:
            quiz_to_instantiate = Quiz.objects.get(id=id)
        except Quiz.DoesNotExist:
            return Response({"error": "Wrong Quiz id."}, status=status.HTTP_400_BAD_REQUEST)

        uid = self.request.query_params.get('uid')
        if not uid:
            return Response({"error": "No user id supplied."}, status=status.HTTP_400_BAD_REQUEST)

        quiz_skill_type = SkillType.objects.get(name=quiz_to_instantiate.skill_type)

        quiz_questions = Question.objects.filter(skill_type=quiz_skill_type.pk)
        quiz_questions_set = set(quiz_question for quiz_question in quiz_questions)
        quiz_questions = sample(quiz_questions_set, k=quiz_to_instantiate.num_of_questions)

        try:
            tbr = QuizInstance.objects.get(user=uid, quiz=quiz_to_instantiate)
            start_time = timezone.now()
            marked = False
            finish_time = None
            score = None
            passed = False
        except QuizInstance.DoesNotExist:
            tbr = QuizInstance(user=uid, quiz=quiz_to_instantiate)

        tbr.save()
        tbr.questions.add(*quiz_questions)

        serializer = QuizInstanceSerializer(tbr)
        return Response(serializer.data)

    def post(self, request, id=None):
        try:
            quiz_instance = QuizInstance.objects.get(id=id)
        except QuizInstance.DoesNotExist:
            return Response({"error": "Wrong Quiz id."}, status=status.HTTP_400_BAD_REQUEST)

        if quiz_instance.marked:
            return Response({"error": "Quiz has already marked and saved."}, status=status.HTTP_400_BAD_REQUEST)

        quiz_instance.finish_time = timezone.now()

        try:
            answers = request.data['answers']
        except KeyError:
            return Response({"error": "Please send your answers to be evaluated."}, status=status.HTTP_400_BAD_REQUEST)

        score = 0
        try:
            for answer in answers:
                atemp = Answer.objects.get(id=answer['aid'])

                if atemp.question.id == answer['qid']:
                    return Response({"error": "Answer doesn't match question."}, status=status.HTTP_400_BAD_REQUEST)

                if atemp.is_correct:
                    score += 1

        except (Answer.DoesNotExist, KeyError):
            return Response({"error": "Invalid answer id."}, status=status.HTTP_400_BAD_REQUEST)

        expected_finish_time = quiz_instance.start_time + timedelta(minutes=quiz_instance.quiz.expected_duration)

        quiz_instance.marked = True
        quiz_instance.score = score
        quiz_instance.passed =\
            (score >= quiz_instance.quiz.pass_score and \
            quiz_instance.finish_time <= expected_finish_time)
        quiz_instance.save()

        return Response({
            "score": score,
            "passed": quiz_instance.passed
        })


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
            if quiz.passed:
                score += quiz.score

        return Response({"score": score})