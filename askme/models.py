import datetime
import random

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from askme.settings import MEDIA_ROOT


class ProfileManager(models.Manager):
    def get_best_members(self, number: int):
        return random.choices(self.select_related("user").all(), k=number)


class Profile(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    nickname = models.CharField(max_length=50, default="nickname")
    avatar = models.ImageField(blank=True, upload_to='', default='shrek.jpeg')

    objects = ProfileManager()

    def __str__(self):
        return f'User nickname: {self.user.username}'


class TagManager(models.Manager):
    def get_most_popular_tags(self, number: int):
        tags = self.all()

        return random.choices(tags, k=number)


class Tag(models.Model):
    title = models.CharField(max_length=40, unique=True)
    objects = TagManager()

    def __str__(self):
        return f'Tag: {self.title}'


class QuestionManager(models.Manager):
    def get_newest_questions(self):
        return self.select_related("sender_id").order_by('-date', '-time')

    def get_questions_by_tag(self, tag: str):
        return self.filter(tag__title__exact=tag).select_related("sender_id")

    def get_most_rated_questions(self):
        return self.select_related("sender_id").order_by('-likes')


class Question(models.Model):
    header = models.TextField()
    body = models.TextField()
    sender_id = models.ForeignKey(Profile, models.SET_NULL, null=True)
    tag = models.ManyToManyField(Tag)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(default=timezone.now().time())
    likes = models.IntegerField(default=0)

    objects = QuestionManager()

    def __str__(self):
        return f'Header: {self.header}'


class QuestionLike(models.Model):
    question_id = models.ForeignKey(Question, models.SET_NULL, null=True)
    user_id = models.ForeignKey(Profile, models.SET_NULL, null=True)
    like = models.BooleanField()

    def __str__(self):
        return f'QuestionLike: {self.like}'


class AnswerManager(models.Manager):
    def get_sorted_answers(self, question_id):
        return self.filter(question_id=question_id).select_related("sender_id").order_by('-likes')


class Answer(models.Model):
    question_id = models.ForeignKey(Question, models.CASCADE)
    body = models.TextField()
    sender_id = models.ForeignKey(Profile, models.SET_NULL, null=True)
    likes = models.IntegerField(default=0)

    objects = AnswerManager()

    def __str__(self):
        return f'Body : {self.body[:20]}...'


class AnswerLike(models.Model):
    answer_id = models.ForeignKey(Answer, models.SET_NULL, null=True)
    user_id = models.ForeignKey(Profile, models.SET_NULL, null=True)
    like = models.BooleanField()

    def __str__(self):
        return f'AnswerLike: {self.like}'

