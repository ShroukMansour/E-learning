from rest_framework import serializers
from company.models import VacancyQuestion, Vacancy, VacancyAnswer, VacancyApplication, SkillType, JobType, Choice


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('choice_text',)


class VacancyQuestionSerializer(serializers.ModelSerializer):
    question_choices = ChoiceSerializer(many=True)

    class Meta:
        model = VacancyQuestion
        fields = ('question_text', 'question_choices')


class VacancySerializer(serializers.ModelSerializer):
    vacancy_questions = VacancyQuestionSerializer(many=True)

    class Meta:
        model = Vacancy
        fields = (
        'id', 'company_id', 'title', 'description', 'requirements', 'benefits', 'salary', 'job_type', 'interest_field',
        'vacancy_questions')

    def create(self, validated_data):
        questions_data = validated_data.pop('vacancy_questions')
        vacancy = Vacancy.objects.create(**validated_data)
        for question_data in questions_data:
            choices = question_data.pop('question_choices')
            q = VacancyQuestion.objects.create(vacancy=vacancy, **question_data)
            for choice in choices:
                Choice.objects.create(question=q, **choice)

        return vacancy
