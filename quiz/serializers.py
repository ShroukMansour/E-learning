from .models import Question, SkillType, Quiz, Answer, QuizInstance
from rest_framework import serializers


class SkillTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillType
        fields = ['name']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['answer_text']


class QuestionSerializer(serializers.ModelSerializer):
    skill_type = SkillTypeSerializer()
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['question_text', 'question_type', 'score', 'skill_type', 'answers']

    def create(self, validated_data):
        skill_type_data = validated_data.pop('skill_type')
        answers_data = validated_data.pop('answers')
        skill_type_obj = SkillType.objects.create( **skill_type_data)
        question = Question.objects.create(skill_type=skill_type_obj, **validated_data)
        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)
        return question


class QuizSerializer(serializers.ModelSerializer):
    skill_type = SkillTypeSerializer()

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'pass_score', 'num_of_questions', 'expected_duration', 'skill_type']

    def create(self, validated_data):
        skill_type_data = validated_data.pop('skill_type')
        skill_type_obj = SkillType.objects.create(**skill_type_data)
        quiz = Quiz.objects.create(skill_type=skill_type_obj, **validated_data)
        return quiz


class QuizInstanceSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = QuizInstance
        fields = ['id', 'quiz', 'questions']
