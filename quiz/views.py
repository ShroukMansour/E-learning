from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from random import sample

from .models import Question, Quiz, QuizInstance, SkillType
from .serializers import QuestionSerializer, QuizSerializer, QuizInstanceSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuizInstances(APIView):
    
    def get(self, request, id=None):
        quiz_to_instantiate = Quiz.objects.filter(id=id)[0]
        quiz_skill_type = SkillType.objects.filter(name=quiz_to_instantiate.skill_type)[0]
        
        quiz_questions = Question.objects.filter(skill_type=quiz_skill_type.pk)
        quiz_questions_set = set(quiz_question for quiz_question in quiz_questions)
        quiz_questions = sample(quiz_questions_set, k=quiz_to_instantiate.num_of_questions)

        tbr = QuizInstance(user=1, quiz=quiz_to_instantiate)  #add user here
        tbr.save()
        tbr.questions.add(*quiz_questions)
        
        serializer = QuizInstanceSerializer(tbr)
        return Response(serializer.data)

