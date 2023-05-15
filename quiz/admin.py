from django.contrib import admin

from .models import MultipleChoiceAnswer, Question, Quiz, TestGroup

admin.site.register(Quiz)
admin.site.register(TestGroup)


class MultipleChoiceAnswerInline(admin.StackedInline):
    model = MultipleChoiceAnswer


class QuestionAdmin(admin.ModelAdmin):
    inlines = [MultipleChoiceAnswerInline]


admin.site.register(Question, QuestionAdmin)
