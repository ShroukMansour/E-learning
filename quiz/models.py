from django.db import models


class SkillType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    skill_type = models.ForeignKey(SkillType, on_delete=models.CASCADE)
    correct_answer_id = models.IntegerField(default=0)
    question_type = models.CharField(max_length=200, default="mcq")
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    answer_text = models.CharField(max_length=1000)

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
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True)
    questions = models.ManyToManyField(Question)
    start_time = models.DateTimeField(auto_now_add=True)

    #stuff filled after finish the quiz
    marked = models.BooleanField(default=False)
    finish_time = models.DateTimeField()
    score = models.IntegerField()

    def __str__(self):
        return str(self.user) + " => " + self.quiz.__str__()
