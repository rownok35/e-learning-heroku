from django.db import models
from App_Login.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class QuizName(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='quiz_creator')
    quizname = models.CharField(
        max_length=264)

    publish_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-publish_date',)

    def __str__(self):
        return self.quizname


class Question(models.Model):
    quiz = models.ForeignKey(
        QuizName, on_delete=models.CASCADE, related_name='quiz_name')
    # user = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name='user_comment')
    question = models.TextField()
    answer_1 = models.TextField()
    answer_2 = models.TextField()
    answer_3 = models.TextField()
    answer_4 = models.TextField()
    correct_answer = models.IntegerField(default=1,
                                         validators=[MaxValueValidator(4), MinValueValidator(1)])

    def __str__(self):
        return self.question
