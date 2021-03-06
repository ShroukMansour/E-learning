from django.db import models


class SkillType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    skill_type = models.ForeignKey(SkillType, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=200, default="MCQ")
    score = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    answer_text = models.CharField(max_length=1000)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    pass_score = models.IntegerField(default=0)
    num_of_questions = models.IntegerField(default=1)
    expected_duration = models.IntegerField(default=10)  # by mins
    skill_type = models.ForeignKey(SkillType, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class QuizInstance(models.Model):
    user = models.IntegerField()    #Foreignkey to the user
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
    questions = models.ManyToManyField(Question)
    start_time = models.DateTimeField(auto_now_add=True)

    #stuff filled after finishing the quiz
    marked = models.BooleanField(default=False)
    finish_time = models.DateTimeField(null=True)
    score = models.IntegerField(null=True)
    passed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + " => " + self.quiz.__str__()


class APILog(models.Model):
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.description