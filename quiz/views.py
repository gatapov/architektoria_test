from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic, View
from django.http.request import HttpRequest

from .models import Question, Quiz, TestGroup


class IndexView(generic.ListView):
    model = Quiz
    template_name = "quiz/index.html"


class MainPage(View):
    def get(self, request: HttpRequest):
        group_list = TestGroup.objects.all()
        return render(
            request,
            "quiz/index.html",
            {"group_list": group_list},
        )


def display_quiz(request: HttpRequest, quiz_id: int):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    question = quiz.question_set.first()
    return redirect(reverse("quiz:display_question", kwargs={"quiz_id": quiz_id, "question_id": question.pk}))


def test_groups(request: HttpRequest, group_slug):
    group = get_object_or_404(TestGroup, slug=group_slug)
    quiz_list = Quiz.objects.filter(test_group=group)

    question_id = request.GET.get('question')

    if question_id is None:
        return render(
            request,
            "quiz/quiz_list.html",
            {"quiz_list": quiz_list, "group_name": group.name},
        )
    else:
        current_question = get_object_or_404(Question, pk=question_id)
        quiz = get_object_or_404(Quiz, pk=current_question.quiz.id)
        questions = quiz.question_set.all()

        next_question = None

        for index, question in enumerate(questions):
            if question.id == int(question_id):
                if index != len(questions) - 1:
                    next_question = questions[index + 1]

        return render(
            request,
            "quiz/display.html",
            {"quiz": current_question.quiz, "question": current_question, "next_question": next_question},
        )


def display_question(request: HttpRequest, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.question_set.all()
    current_question, next_question = None, None
    for ind, question in enumerate(questions):
        if question.pk == question_id:
            current_question = question
            if ind != len(questions) - 1:
                next_question = questions[ind + 1]

    return render(
        request,
        "quiz/display.html",
        {"quiz": quiz, "question": current_question, "next_question": next_question},
    )


def grade_question(request: HttpRequest, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answer = question.get_answer()

    if answer is None:
        return render(request, "quiz/partial.html", {"error": "Question must have an answer"}, status=422)

    is_correct = answer.is_correct(request.POST.get("answer"))

    return render(
        request,
        "quiz/partial.html",
    )
