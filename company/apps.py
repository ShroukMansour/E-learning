from django.apps import AppConfig


class CompanyConfig(AppConfig):
    name = 'company'

    def ready(self):
        from .models import JobType
        if len(JobType.objects.all()) != 3:
            JobType.objects.create(name='Full Time')
            JobType.objects.create(name='Half Time')
            JobType.objects.create(name='Intern')
