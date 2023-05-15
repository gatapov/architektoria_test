from django.urls import path

from . import views

app_name = "quiz"

urlpatterns = [
    path("", views.MainPage.as_view(), name="index"),
    path("quiz/", views.MainPage.as_view(), name="quiz_list"),
    path("quiz/<str:group_slug>/", views.test_groups, name="test_groups"),

    path("questions/<int:question_id>/grade/", views.grade_question, name="grade_question"),
]
