from django.db import models
from django.utils.text import slugify
from django.conf import settings
from courses.models import Course


class Quiz(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="quizzes",
        null=True, blank=True
    )
    name = models.CharField(max_length=75)
    description = models.CharField(max_length=75)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions"
    )
    text = models.CharField(max_length=75)
    correct_answer = models.CharField(max_length=75)
    marks = models.IntegerField(default=1)
    option_a = models.CharField(max_length=75)
    option_b = models.CharField(max_length=75)
    option_c = models.CharField(max_length=75)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.text)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text


# ---------------------------------------------------
# NEW MODELS FOR SAVING STUDENT QUIZ ATTEMPTS
# ---------------------------------------------------

class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    obtained_marks = models.IntegerField(default=0)
    total_marks = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.name}"


class QuestionResult(models.Model):
    attempt = models.ForeignKey(
        QuizAttempt,
        on_delete=models.CASCADE,
        related_name="results"
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    marks = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.question.text} ({self.attempt.user.username})"
