from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.db import IntegrityError

from askme.models import Profile, Question, Tag, Answer


class EditFrom(forms.ModelForm):
    nickname = forms.CharField(min_length=3, max_length=50)
    email = forms.CharField(widget=forms.EmailInput)

    class Meta:
        model = Profile
        fields = ["nickname", "avatar"]

    def clean_email(self):
        validate_email(self.data["email"])
        return self.data["email"]

    def clean_avatar(self):
        if self.files.get("avatar") is None:
            raise ValidationError("Please upload avatar")

        return self.files.get("avatar")

    def update_user(self, user: User):
        user.email = self.cleaned_data["email"]
        user.profile.nickname = self.cleaned_data["nickname"]
        user.profile.avatar = self.cleaned_data["avatar"]
        user.save()
        user.profile.save()


class AnswerForm(forms.Form):
    body = forms.CharField(min_length=5, widget=forms.Textarea)

    class Meta:
        model = Answer
        fields = ["body"]

    def save(self, user, question_id):
        answer = Answer(body=self.cleaned_data["body"])
        answer.sender_id = user.profile
        answer.question_id = Question.objects.get(id=question_id)
        answer.save()
        return answer


class QuestionForm(forms.Form):
    header = forms.CharField(min_length=5)
    body = forms.CharField(min_length=5, widget=forms.Textarea)
    tag = forms.CharField(min_length=3)

    class Meta:
        model = Question
        fields = ["header", "body", "tag"]

    def clean_tag(self):
        MAX_LENGTH = 30
        length = sum(map(lambda x: len(x), self.cleaned_data["tag"].split()))
        if length > MAX_LENGTH:
            raise ValidationError(f"Length of tags is too big, max = {MAX_LENGTH}, yours = {length}")

        return self.cleaned_data["tag"]

    def save(self, user: User):
        question = Question(header=self.cleaned_data["header"], body=self.cleaned_data["body"])
        question.sender_id = user.profile
        tags = self.cleaned_data["tag"].split()
        question.save()
        for tag_title in tags:
            tag_item = Tag(title=tag_title)
            try:
                tag_item.save()
            except IntegrityError:
                tag_item = Tag.objects.get(title=tag_item.title)
            question.tag.add(tag_item)
        return question


class LoginForm(forms.Form):
    username = forms.CharField(min_length=6, max_length=50)
    password = forms.CharField(min_length=8, max_length=50, widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    username = forms.CharField(min_length=5, max_length=50)
    email = forms.CharField(widget=forms.EmailInput)
    nickname = forms.CharField(min_length=3, max_length=50)
    password = forms.CharField(min_length=8, max_length=50, widget=forms.PasswordInput)
    password_check = forms.CharField(min_length=8, max_length=50, widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ["nickname", "avatar"]

    def clean_username(self):
        if any(filter(lambda user: user.username == self.data['username'], User.objects.all())):
            raise ValidationError("Username already exists")

        return self.data["username"]

    def clean_email(self):
        validate_email(self.data["email"])
        return self.data["email"]

    def clean_nickname(self):
        if self.data["username"] == self.data["nickname"]:
            raise ValidationError("Nickname and login are similar")

        return self.data["nickname"]

    def clean_avatar(self):
        if self.files.get("avatar", "") == "":
            raise ValidationError("Please upload avatar")

        return self.files.get("avatar")

    def clean(self):
        password_1 = self.data.get("password", "")
        password_2 = self.data.get("password_check", "")

        if password_1 != password_2:
            raise ValidationError("Passwords are different")

        return self.cleaned_data

    def save(self):
        self.cleaned_data.pop("password_check")
        # костыль:
        profile = Profile(avatar=self.cleaned_data["avatar"], nickname=self.cleaned_data["nickname"])
        self.cleaned_data.pop("avatar")
        self.cleaned_data.pop("nickname")
        user = User.objects.create_user(**self.cleaned_data)
        profile.user = user
        profile.save()
        # конец костыля
        return user

