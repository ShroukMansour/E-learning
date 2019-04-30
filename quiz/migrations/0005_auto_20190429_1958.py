# Generated by Django 2.1.7 on 2019-04-29 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20190426_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(default='MCQ', max_length=200),
        ),
        migrations.AlterField(
            model_name='question',
            name='score',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='quizinstance',
            name='passed',
            field=models.BooleanField(default=False),
        ),
    ]