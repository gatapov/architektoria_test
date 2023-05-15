import typing

from django.contrib.postgres import fields
from django.db import models


class TestGroup(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(default='')

    objects = models.Manager()

    def __str__(self):
        return self.name


class Quiz(models.Model):
    name = models.CharField(max_length=100)
    test_group = models.ForeignKey(TestGroup, on_delete=models.DO_NOTHING, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    prompt = models.CharField(max_length=200)

    objects = models.Manager()

    def __str__(self):
        return self.prompt

    def get_answer(self) -> typing.Union["Answer", None]:
        return getattr(self, "multiplechoiceanswer", None) or getattr(self, "freetextanswer", None)


class Answer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    correct_answer = models.CharField(max_length=200)

    objects = models.Manager()

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.correct_answer

    def is_correct(self, user_answer) -> bool:
        return user_answer == self.correct_answer


class FreeTextAnswer(Answer):
    case_sensitive = models.BooleanField(default=False)

    objects = models.Manager()

    def is_correct(self, user_answer) -> bool:
        if not self.case_sensitive:
            return user_answer.lower() == self.correct_answer.lower()
        return user_answer == self.correct_answer


class MultipleChoiceAnswer(Answer):
    choices = fields.ArrayField(models.CharField(max_length=200, blank=True))

    objects = models.Manager()

    def __str__(self) -> str:
        return f"{self.correct_answer} from {self.choices}"
