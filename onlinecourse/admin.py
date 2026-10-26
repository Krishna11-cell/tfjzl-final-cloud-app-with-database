```python
from django.contrib import admin
from .models import (
    Choice,
    Course,
    Instructor,
    Learner,
    Lesson,
    Question,
    Submission,
)


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]
    list_display = ("name", "description")
    search_fields = ("name", "description")


class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "course", "grade")
    list_filter = ("course",)
    inlines = [ChoiceInline]


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("choice_text", "question", "is_correct")
    list_filter = ("is_correct",)


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Submission)
```
