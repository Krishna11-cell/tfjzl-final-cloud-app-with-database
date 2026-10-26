from django.contrib import admin
from .models import Course, Lesson, Question, Choice, Submission

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    inlines = [QuestionInline]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    list_filter = ("course",)
    ordering = ("course", "order")

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "course", "grade")
    list_filter = ("course",)
    inlines = [ChoiceInline]

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("text", "question", "is_correct")
    list_filter = ("is_correct",)

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "score", "total_questions", "submitted_at")
    list_filter = ("course", "submitted_at")
    readonly_fields = ("submitted_at",)
