from django.db import models
from quiz.models import SkillType


class Company(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, default='Egypt')
    num_of_employees= models.IntegerField(default=10)
    email = models.CharField(max_length=200, default="company@gmail.com")
    interest_fields = models.ManyToManyField(SkillType)


class JobType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name





class Vacancy(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000, default='Vacancy description')
    requirments = models.CharField(max_length=10000, default='Vacancy requirments')
    benefits = models.CharField(max_length=500)
    salary = models.IntegerField(default=1000)
    job_type = models.OneToOneField(JobType, on_delete=models.CASCADE)
    interest_field = models.OneToOneField(SkillType, on_delete=models.CASCADE)


class VacancyQuestion(models.Model):
    question_text = models.CharField(max_length=200)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    def __str__(self):
        return self.question_text


class VacancyApplication(models.Model):
    user_id = models.IntegerField(null=False)


class VacancyAnswer(models.Model):
    question = models.ForeignKey(VacancyQuestion, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=1000)
    vacancy_application = models.ForeignKey(VacancyApplication, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer_text



