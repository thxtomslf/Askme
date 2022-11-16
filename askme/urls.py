"""askme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from app import views


urlpatterns = [
    path('', views.new_questions, kwargs={'number_of_questions_block': 0}, name="new_questions"),
    path('<int:number_of_questions_block>', views.new_questions,
         name="new_questions"),
    path('hot', views.hot_questions, name="hot_questions"),
    path('tag/<str:tag_title>', views.questions_by_tag, name="questions_by_tag"),
    path('login', views.login, name="login"),
    path('signup', views.register, name="signup"),
    path('settings', views.register, name="settings"),
    path('ask', views.create_question, name="ask_question"),
    path('question/<int:questionId>', views.question, name="question")
]
