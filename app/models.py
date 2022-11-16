import itertools
import random

from django.db import models

# Create your models here.

titles = itertools.cycle(["Swamp question", "Princess", "Why is Farquaad so short?", "What is the size of Shrek's...?"])

texts = itertools.cycle(["why are you on my swamp? go away. i don't wanna see you here. take it."
                         " why are you on my swamp? go away."" i don't wanna see you here.why are"
                         " you on my swamp? go away. i don't wanna see you here. take it. why are"
                         " you on my swamp? go away. i don't wanna see you here.why are you on my swamp?"
                         " go away. i don't wanna see"" you here. take it. why are you on my swamp? go away."
                         " i don't wanna see you here.why are you on my swamp? go away. i don't wanna see you here. take it."
                         " why are you on my swamp? go away."" i don't wanna see you here.why are"
                         " you on my swamp? go away. i don't wanna see you here. take it. why are"
                         " you on my swamp? go away. i don't wanna see you here.why are you on my swamp?"
                         " go away. i don't wanna see"" you here. take it. why are you on my swamp? go away."
                         " i don't wanna see you here."])

tags = itertools.cycle([["Swamp", "go away"], ["escape", "charming", "Donkey"], ["growth"], ["Kill_ogre"]])

users = itertools.cycle(["Shrek", "Fiona", "Donkey", "XXXX"])


QUESTIONS = [{"user_name": next(users), "rating": random.randint(0, 100), "id": i, "title": next(titles), "text": next(texts), "tags": next(tags)} for i in range(12)]

ANSWERS = [{"user_name": next(users), "rating": random.randint(0, 100), "text": next(texts)} for i in range(4)]

BEST_MEMBERS = ["Donkey", "Shrek", "Fiona", "Pinokio"]

POPULAR_TAGS = ["Swamp", "Donkey", "Charming", "Kill_ogre", "Pretty_princess"]
