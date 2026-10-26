
from django.contrib import admin
from .models import (
    Course,
    Lesson,
    Instructor,
    Learner,
    Enrollment,
    Question,
    Choice,
    Submission,
)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "course", "grade")
    list_filter = ("course",)
    search_fields = ("text",)
    inlines = [ChoiceInline]


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("text", "question", "is_correct")
    list_filter = ("is_correct",)


class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    list_filter = ("course",)
    ordering = ("course", "order")


class CourseAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    inlines = [QuestionInline]


class InstructorAdmin(admin.ModelAdmin):
    list_display = ("user", "full_time", "total_learners")


class LearnerAdmin(admin.ModelAdmin):
    list_display = ("user", "occupation", "social_link")
    list_filter = ("occupation",)


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "date_enrolled", "mode", "rating")
    list_filter = ("course", "mode")


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "enrollment", "score", "submitted_at")
    list_filter = ("submitted_at",)
    filter_horizontal = ("choices",)
    readonly_fields = ("submitted_at",)


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Learner, LearnerAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Submission, SubmissionAdmin)
