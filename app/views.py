from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponseNotFound

from askme.models import Question, Tag, Profile, Answer


def hot_questions(request):
    top_rate_questions = Question.objects.get_most_rated_questions()
    paginator = Paginator(top_rate_questions, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    popular_tags = Tag.objects.get_most_popular_tags(5)

    best_members = Profile.objects.get_best_members(5)

    context = {"page_obj": page_obj, "best_members": best_members, "popular_tags": popular_tags}
    return render(request, "../templates/_hot_questions.html", context=context)


def questions_by_tag(request, tag_title: str):
    tagged_questions = Question.objects.get_questions_by_tag(tag_title)
    paginator = Paginator(tagged_questions, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    popular_tags = Tag.objects.get_most_popular_tags(5)

    best_members = Profile.objects.get_best_members(5)

    context = {"tag": tag_title, "page_obj": page_obj, "best_members": best_members, "popular_tags": popular_tags}
    return render(request, "../templates/_questions_by_tag.html", context=context)


def new_questions(request):
    questions = Question.objects.get_newest_questions()
    paginator = Paginator(questions, 10)
    print(questions[0].sender_id.avatar.url)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    popular_tags = Tag.objects.get_most_popular_tags(5)

    best_members = Profile.objects.get_best_members(5)

    context = {"page_obj": page_obj, "best_members": best_members, "popular_tags": popular_tags}
    return render(request, "../templates/_new_questions.html", context=context)


def question(request, questionId: int):
    try:
        question = Question.objects.get_newest_questions().get(id=questionId)
    except Question.DoesNotExist:
        return HttpResponseNotFound()

    answers = Answer.objects.get_sorted_answers(question)

    popular_tags = Tag.objects.get_most_popular_tags(5)

    best_members = Profile.objects.get_best_members(5)

    context = {"question": question, "answers": answers, "best_members": best_members,
               "popular_tags": popular_tags}

    return render(request, "../templates/_question_page.html", context=context)


def login(request):
    popular_tags = Tag.objects.get_most_popular_tags(5)

    best_members = Profile.objects.get_best_members(5)

    context = {"best_members": best_members, "popular_tags": popular_tags}
    return render(request, "../templates/_login.html", context=context)


def register(request):
    popular_tags = Tag.objects.get_most_popular_tags(5)

    best_members = Profile.objects.get_best_members(5)

    context = {"best_members": best_members, "popular_tags": popular_tags}
    return render(request, "../templates/_register.html", context=context)


def create_question(request):
    popular_tags = Tag.objects.get_most_popular_tags(5)

    best_members = Profile.objects.get_best_members(5)

    context = {"best_members": best_members, "popular_tags": popular_tags}
    return render(request, "../templates/_question_creating.html", context=context)


def settings(request):
    popular_tags = Tag.objects.get_most_popular_tags(5)

    best_members = Profile.objects.get_best_members(5)

    context = {"best_members": best_members, "popular_tags": popular_tags}
    return render(request, "../templates/_settings.html", context=context)

