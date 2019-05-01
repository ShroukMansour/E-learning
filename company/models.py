from django.db import models
from quiz.models import SkillType


# class Company(models.Model):
#     name = models.CharField(max_length=200)
#     location = models.CharField(max_length=200, default='Egypt')
#     num_of_employees= models.IntegerField(default=10)
#     email = models.CharField(max_length=200, default="company@gmail.com")
#     interest_fields = models.ManyToManyField(SkillType)
#

class JobType(models.Model):
    name = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    company_id = models.IntegerField(null=False)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000, default='Vacancy description')
    requirements = models.CharField(max_length=10000, default='Vacancy requirments')
    benefits = models.CharField(max_length=500, default="benefits")
    salary = models.IntegerField(default=0)
    job_types = (('Full Time', 'Full Time'), ("Part Time", "Part Time"), ("Intern", "Intern"))
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    # job_type = models.CharField(max_length=15, choices=job_types)
    interest_field = models.ForeignKey(SkillType, on_delete=models.CASCADE)


class VacancyQuestion(models.Model):
    question_text = models.CharField(max_length=200)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="vacancy_questions")

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    class Meta:
        unique_together = (('choice_text', 'question'))

    choice_text = models.CharField(max_length=200)
    question = models.ForeignKey(VacancyQuestion, on_delete=models.CASCADE, related_name='question_choices')


class VacancyApplication(models.Model):
    user_id = models.IntegerField(null=False)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)


class VacancyAnswer(models.Model):
    question = models.ForeignKey(VacancyQuestion, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=1000)
    vacancy_application = models.ForeignKey(VacancyApplication, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer_text
