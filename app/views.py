from django.shortcuts import render
from django.http import HttpResponseNotFound

from app.models import QUESTIONS, BEST_MEMBERS, POPULAR_TAGS, ANSWERS


# Create your views here.


def new_questions(request, number_of_questions_block: int):
    context = {"questions": QUESTIONS, "best_members": BEST_MEMBERS, "popular_tags": POPULAR_TAGS}
    return render(request, "../templates/_new_questions.html", context=context)


def question(request, questionId: int):
    if not any(map(lambda item: item["id"] == questionId, QUESTIONS)):
        return HttpResponseNotFound()
    context = {"question": QUESTIONS[questionId], "answers": ANSWERS, "best_members": BEST_MEMBERS,
               "popular_tags": POPULAR_TAGS}

    return render(request, "../templates/_question_page.html", context=context)


def hot_questions(request):
    top_rate_questions = sorted(QUESTIONS, key=lambda x: x["rating"], reverse=True)
    context = {"questions": top_rate_questions, "best_members": BEST_MEMBERS, "popular_tags": POPULAR_TAGS}
    return render(request, "../templates/_hot_questions.html", context=context)


def questions_by_tag(request, tag_title: str):
    tagged_questions = filter(lambda item: tag_title in item["tags"], QUESTIONS)
    context = {"tag": tag_title, "questions": tagged_questions, "best_members": BEST_MEMBERS, "popular_tags": POPULAR_TAGS}
    return render(request, "../templates/_questions_by_tag.html", context=context)


def login(request):
    context = {"best_members": BEST_MEMBERS, "popular_tags": POPULAR_TAGS}
    return render(request, "../templates/_login.html", context=context)


def register(request):
    context = {"best_members": BEST_MEMBERS, "popular_tags": POPULAR_TAGS}
    return render(request, "../templates/_register.html", context=context)


def create_question(request):
    context = {"best_members": BEST_MEMBERS, "popular_tags": POPULAR_TAGS}
    return render(request, "../templates/_question_creating.html", context=context)


def settings(request):
    context = {"best_members": BEST_MEMBERS, "popular_tags": POPULAR_TAGS}
    return render(request, "../templates/_settings.html", context=context)

