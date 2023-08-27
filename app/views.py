from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponseNotAllowed, HttpResponse
from django.urls import reverse
from django.contrib.auth import login as log_in


from app.forms import LoginForm, RegisterForm, QuestionForm, AnswerForm, EditFrom
from askme.models import Question, Tag, Profile, Answer


def hot_questions(request):
    top_rate_questions = Question.objects.get_most_rated_questions()
    paginator = Paginator(top_rate_questions, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    popular_tags = Tag.objects.get_most_popular_tags(5)

    best_members = Profile.objects.get_best_members(5)

    context = {"page_obj": page_obj, "best_members": best_members, "popular_tags": popular_tags, "user": request.user,
               "current_path": request.path}
    return render(request, "../templates/_hot_questions.html", context=context)


def questions_by_tag(request, tag_title: str):
    tagged_questions = Question.objects.get_questions_by_tag(tag_title)
    paginator = Paginator(tagged_questions, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    popular_tags = Tag.objects.get_most_popular_tags(5)

    best_members = Profile.objects.get_best_members(5)

    context = {"tag": tag_title, "page_obj": page_obj, "best_members": best_members, "popular_tags": popular_tags,
               "user": request.user, "current_path": request.path}
    return render(request, "../templates/_questions_by_tag.html", context=context)


def new_questions(request):
    questions = Question.objects.get_newest_questions()
    paginator = Paginator(questions, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    popular_tags = Tag.objects.get_most_popular_tags(5)
    best_members = Profile.objects.get_best_members(5)
    context = {"page_obj": page_obj, "best_members": best_members, "popular_tags": popular_tags,
               "user": request.user, "current_path": request.path}
    return render(request, "../templates/_new_questions.html", context=context)


def question(request, questionId: int):
    if request.method == "GET":
        answer_form = AnswerForm()
    elif request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(reverse("login") + "?continue=" + request.path)

        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(request.user, question_id=questionId)
            return redirect(request.path + "#" + str(answer.id))
    else:
        return HttpResponseNotAllowed(["POST", "GET"])

    try:
        question = Question.objects.get(id=questionId)
    except Question.DoesNotExist:
        return HttpResponseNotFound()

    answers = Answer.objects.get_sorted_answers(question)

    popular_tags = Tag.objects.get_most_popular_tags(5)

    best_members = Profile.objects.get_best_members(5)

    context = {"question": question, "answers": answers, "best_members": best_members, "form": answer_form,
               "popular_tags": popular_tags, "user": request.user, "question_id": questionId, "current_path": request.path}

    return render(request, "../templates/_question_page.html", context=context)


def login(request):
    if request.method == "GET":
        user_form = LoginForm()
    elif request.method == "POST":
        user_form = LoginForm(request.POST)
        if user_form.is_valid():
            user = auth.authenticate(request=request.POST, **user_form.cleaned_data)
            if user:
                log_in(request, user)
                return redirect(request.GET.get("continue", "/"))
            else:
                user_form.add_error(field="username", error="Wrong username or password")
    else:
        return HttpResponseNotAllowed(["POST", "GET"])

    popular_tags = Tag.objects.get_most_popular_tags(5)

    best_members = Profile.objects.get_best_members(5)
    context = {"best_members": best_members, "popular_tags": popular_tags, 'form': user_form,
               "redirect_param": request.GET.get("continue", ""), "current_path": request.path}
    return render(request, "../templates/_login.html", context=context)


def register(request):
    if request.method == "GET":
        register_form = RegisterForm()
    elif request.method == "POST":
        register_form = RegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            if user:
                return redirect(reverse("login"))
            else:
                register_form.add_error(field=None, error=register_form.errors)
    else:
        return HttpResponseNotAllowed(["POST", "GET"])

    popular_tags = Tag.objects.get_most_popular_tags(5)

    best_members = Profile.objects.get_best_members(5)

    context = {"best_members": best_members, "popular_tags": popular_tags, "form": register_form,
               "user": request.user, "current_path": request.path}
    return render(request, "../templates/_register.html", context=context)


def logout_user(request):
    logout(request)
    return redirect(request.GET["continue"])


@login_required(login_url='login', redirect_field_name="continue")
def create_question(request):
    if request.method == "GET":
        question_form = QuestionForm()
    elif request.method == "POST":
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            added_question = question_form.save(request.user)
            return redirect("question/" + str(added_question.id))
    else:
        return HttpResponseNotAllowed(["POST", "GET"])
    popular_tags = Tag.objects.get_most_popular_tags(5)

    best_members = Profile.objects.get_best_members(5)

    context = {"best_members": best_members, "popular_tags": popular_tags, "form": question_form, "user": request.user,
               "current_path": request.path}
    return render(request, "../templates/_question_creating.html", context=context)


@login_required(login_url="login", redirect_field_name="continue")
def settings(request):
    if request.method == "GET":
        settings_form = EditFrom()
    elif request.method == "POST":
        settings_form = EditFrom(request.POST, request.FILES)
        if settings_form.is_valid():
            settings_form.update_user(request.user)
            return redirect(reverse("settings"))
    else:
        return HttpResponseNotAllowed(["POST", "GET"])

    popular_tags = Tag.objects.get_most_popular_tags(5)

    best_members = Profile.objects.get_best_members(5)
    context = {"best_members": best_members, "popular_tags": popular_tags, "user": request.user,
               "current_path": request.path, "form": settings_form}
    return render(request, "../templates/_settings.html", context=context)

