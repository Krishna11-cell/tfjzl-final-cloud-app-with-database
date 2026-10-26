
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
    return render(
        request,
        "onlinecourse/course_details_bootstrap.html",
        {"course": course},
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

    submission = Submission.objects.create(enrollment=enrollment)

    selected_choices = []
    for key, value in request.POST.items():
        if key.startswith("choice_"):
            try:
                choice_id = int(value)
            except (TypeError, ValueError):
                continue

            choice = Choice.objects.filter(
                pk=choice_id,
                question__course=course,
            ).first()

            if choice:
                selected_choices.append(choice)

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
    total_score = 0
    possible_score = 0

    for question in course.question_set.prefetch_related("choice_set").all():
        question_choices = list(question.choice_set.all())
        question_choice_ids = {
            choice.id for choice in question_choices
        }
        selected_for_question = selected_ids & question_choice_ids

        question_score = question.is_get_score(selected_for_question)
        total_score += question_score
        possible_score += question.grade

        results.append({
            "question": question,
            "selected_choices": [
                choice for choice in question_choices
                if choice.id in selected_ids
            ],
            "correct_choices": [
                choice for choice in question_choices
                if choice.is_correct
            ],
            "is_correct": question_score == question.grade,
        })

    return render(
        request,
        "onlinecourse/exam_result.html",
        {
            "course": course,
            "submission": submission,
            "results": results,
            "grade": total_score,
            "possible": possible_score,
            "total_score": total_score,
            "possible_score": possible_score,
        },
    )
