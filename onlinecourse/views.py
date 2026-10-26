
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Course, Enrollment, Question, Choice, Submission


def course_list(request):
    return render(
        request,
        "onlinecourse/course_list.html",
        {"courses": Course.objects.all()},
    )


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    questions = course.questions.prefetch_related("choices").all()

    return render(
        request,
        "onlinecourse/course_details_bootstrap.html",
        {
            "course": course,
            "lessons": course.lessons.all(),
            "questions": questions,
        },
    )


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method != "POST":
        return redirect("course_details", course_id=course.id)

    enrollment, _ = Enrollment.objects.get_or_create(
        user=request.user,
        course=course,
        defaults={"mode": Enrollment.AUDIT},
    )

    questions = course.questions.prefetch_related("choices").all()
    selected_choices = []
    score = 0

    for question in questions:
        choice_id = request.POST.get(f"question_{question.id}")

        if not choice_id:
            continue

        choice = question.choices.filter(pk=choice_id).first()

        if choice:
            selected_choices.append(choice)
            if choice.is_correct:
                score += question.grade

    submission = Submission.objects.create(
        enrollment=enrollment,
        score=score,
    )
    submission.choices.set(selected_choices)

    return redirect(
        "show_exam_result",
        course_id=course.id,
        submission_id=submission.id,
    )


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(
        Submission,
        pk=submission_id,
        enrollment__user=request.user,
        enrollment__course=course,
    )

    selected_ids = set(
        submission.choices.values_list("id", flat=True)
    )

    results = []
    for question in course.questions.prefetch_related("choices").all():
        choices = list(question.choices.all())
        correct_choices = [c for c in choices if c.is_correct]
        selected = [c for c in choices if c.id in selected_ids]

        results.append({
            "question": question,
            "choices": choices,
            "selected_choices": selected,
            "correct_choices": correct_choices,
            "is_correct": bool(
                correct_choices
                and any(c.id in selected_ids for c in correct_choices)
            ),
        })

    return render(
        request,
        "onlinecourse/exam_result.html",
        {
            "course": course,
            "submission": submission,
            "results": results,
        },
    )
