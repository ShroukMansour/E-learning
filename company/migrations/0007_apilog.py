# Generated by Django 2.2 on 2019-05-01 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0006_choice'),
    ]

    operations = [
        migrations.CreateModel(
            name='APILog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=1000)),
            ],
        ),
    ]