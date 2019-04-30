from .models import Question, SkillType, Quiz, Answer, QuizInstance
from rest_framework import serializers


class SkillTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillType
        fields = ['id', 'name']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer_text', 'is_correct']
        extra_kwargs = {
            'is_correct': {'write_only': True},
        }


class QuestionSerializer(serializers.ModelSerializer):
    skill_type = SkillTypeSerializer()
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'score', 'skill_type', 'answers']

    def create(self, validated_data):
        skill_type_data = validated_data.pop('skill_type')
        answers_data = validated_data.pop('answers')
        skill_type_obj = SkillType.objects.get_or_create(**skill_type_data)[0]
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
        skill_type_obj = SkillType.objects.get_or_create(**skill_type_data)[0]
        quiz = Quiz.objects.create(skill_type=skill_type_obj, **validated_data)
        return quiz


class QuizInstanceSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    expected_duration = serializers.ReadOnlyField(source='quiz.expected_duration')

    class Meta:
        model = QuizInstance
        fields = ['id', 'questions', 'expected_duration']
        depth = 1
