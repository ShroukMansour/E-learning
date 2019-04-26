# Generated by Django 2.1.7 on 2019-04-26 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_auto_20190426_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizinstance',
            name='passed',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='quizinstance',
            name='quiz',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.Quiz'),
        ),
    ]
