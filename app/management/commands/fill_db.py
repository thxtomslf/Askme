import datetime
import pathlib
import random
from os import listdir
from typing import List

import random_word
from django.core.management.base import BaseCommand
from askme.models import Profile, Question, Answer, Tag, AnswerLike, QuestionLike
from random_word import RandomWords
from askme.settings import MEDIA_ROOT
from django.contrib.auth.models import User
from faker import Faker


class Command(BaseCommand):
    help = "Fills db with random values."
    randomizer = random_word.RandomWords()
    dater = Faker()

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Filling ratio')

    def handle(self, *args, **options):
        ratio = options['ratio']
        text = list(set([self.randomizer.get_random_word() + "ing" for _ in range(ratio)]))
        ratio = len(text)

        users = self.fill_users(ratio, text)
        print("[DEBUG] Users written")
        questions = self.fill_questions(ratio, text, text, users)
        print("[DEBUG] Question, likes and tags written")
        self.fill_answers(ratio, text, users, questions)
        print("[DEBUG] Answers, likes and tags written")

    def fill_users(self, ratio: int, text: List[str]):
        profiles = []
        users = []
        files = listdir(MEDIA_ROOT + "\\image")
        for i in range(ratio):
            word = text[i]
            users.append(User(last_login=datetime.datetime.now(),
                              password=word,
                              email=f"{word}@mail.ru",
                              username=word.capitalize())
                         )
            profiles.append(Profile(
                avatar=random.choice(files),
                user=users[-1])
            )

        for i in range(0, len(users), 500):
            if i + 500 >= len(users):
                User.objects.bulk_create(users[i:len(users)])
            else:
                User.objects.bulk_create(users[i:i + 500])

        for i in range(0, len(profiles), 500):
            if i + 500 >= len(profiles):
                Profile.objects.bulk_create(profiles[i:len(profiles)])
            else:
                Profile.objects.bulk_create(profiles[i:i + 500])

        return profiles

    def fill_questions(self, ratio: int, tags_titles: List[str], text: List[str], users):
        questions = []
        rating = []
        tags = []
        for i in range(ratio * 10):
            # making common question data
            header = ' '.join(random.choices(text, k=20)).capitalize() + "?"
            body = ' '.join(random.choices(text, k=150)).capitalize() + '.'
            likes = random.randint(0, int((i ** 0.25) + 40))
            date = self.dater.date_between_dates(date_start=datetime.date(2015, 1, 1), date_end=datetime.date.today())
            user_id = users[random.randint(0, len(users) - 1)]

            question = Question(header=header,
                                body=body,
                                likes=likes,
                                date=date,
                                sender_id=user_id)
            questions.append(question)

            # making likes
            for __ in range(likes):
                rating.append(QuestionLike(
                    like=random.randint(0, 1),
                    question_id=question,
                    user_id=users[random.randint(0, len(users) - 1)])
                )
        print(len(rating))
        for i in range(0, len(questions), 500):
            if i + 500 >= len(questions):
                Question.objects.bulk_create(questions[i:len(questions)])
            else:
                Question.objects.bulk_create(questions[i:i + 500])

        for i in range(ratio):
            tag = Tag(title=tags_titles[i])
            tags.append(tag)

        for i in range(0, len(tags), 500):
            if i + 500 >= len(tags):
                Tag.objects.bulk_create(tags[i:len(tags)])
            else:
                Tag.objects.bulk_create(tags[i:i + 500])

        for question in questions:
            tags_number = random.randint(1, 4) if len(tags) >= 4 else random.randint(1, len(tags))
            tag_obj = random.choices(tags, k=tags_number)
            for tag in tag_obj:
                question.tag.add(tag)

        for i in range(0, len(rating) - 1, 500):
            if i + 500 >= len(rating):
                QuestionLike.objects.bulk_create(rating[i:len(rating)])
            else:
                QuestionLike.objects.bulk_create(rating[i:i + 500])
        return questions

    def fill_answers(self, ratio, text: List[str], users, questions):
        answers = []
        rating = []
        for i in range(ratio * 100):
            question_id = questions[random.randint(0, len(questions) - 1)]
            body = ' '.join(random.choices(text, k=random.randint(50, 150))).capitalize() + '.'
            user_id = users[random.randint(0, len(users) - 1)]
            likes = random.randint(0, int((i ** 0.25) + 40))

            answer = Answer(body=body, sender_id=user_id, question_id=question_id, likes=likes)
            answers.append(answer)

            # making likes
            for __ in range(likes):
                rating.append(AnswerLike(
                    like=random.randint(0, 1),
                    answer_id=answer,
                    user_id=users[random.randint(0, len(users) - 1)])
                )
        for i in range(0, len(answers) - 1, 500):
            if i + 500 >= len(answers):
                Answer.objects.bulk_create(answers[i:len(answers)])
            else:
                Answer.objects.bulk_create(answers[i:i + 500])
        for i in range(0, len(rating) - 1, 500):
            if i + 500 >= len(answers):
                AnswerLike.objects.bulk_create(rating[i:len(rating)])
            else:
                AnswerLike.objects.bulk_create(rating[i:i + 500])
