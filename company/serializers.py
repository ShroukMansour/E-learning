from rest_framework import serializers
from company.models import VacancyQuestion, Vacancy, VacancyAnswer, VacancyApplication, SkillType, JobType, Choice
from quiz.serializers import SkillTypeSerializer


class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobType
        fields = ['name']


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('choice_text',)


class VacancyQuestionSerializer(serializers.ModelSerializer):
    question_choices = ChoiceSerializer(many=True)

    class Meta:
        model = VacancyQuestion
        fields = ('id', 'question_text', 'question_choices')


class VacancySerializer(serializers.ModelSerializer):
    vacancy_questions = VacancyQuestionSerializer(many=True)
    interest_field = SkillTypeSerializer()

    # job_type = JobTypeSerializer()

    class Meta:
        model = Vacancy
        fields = (
            'id', 'company_id', 'title', 'description', 'requirements', 'benefits',
            'salary', 'job_type', 'interest_field', 'vacancy_questions')

    def create(self, validated_data):
        questions_data = validated_data.pop('vacancy_questions')
        interest_field_data = validated_data.pop('interest_field')
        interest_field_obj = SkillType.objects.get_or_create(**interest_field_data)[0]
        vacancy = Vacancy.objects.create(interest_field=interest_field_obj, **validated_data)
        for question_data in questions_data:
            choices = question_data.pop('question_choices')
            q = VacancyQuestion.objects.create(vacancy=vacancy, **question_data)
            for choice in choices:
                Choice.objects.create(question=q, **choice)

        return vacancy


class VacancyAnswerSerializer(serializers.ModelSerializer):
    question = VacancyQuestionSerializer()

    class Meta:
        model = VacancyAnswer
        fields = ["question", "answer_text"]


class VacancyApplicationSerializer(serializers.ModelSerializer):
    vacancy_id = serializers.ReadOnlyField(source="vacancy.id")

    class Meta:
        model = VacancyApplication
        fields = ["vacancy_id", "user_id"]
