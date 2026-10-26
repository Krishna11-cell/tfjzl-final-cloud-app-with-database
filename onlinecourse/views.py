from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Course, Submission

def course_list(request):
    return render(request, "onlinecourse/course_list.html", {"courses": Course.objects.all()})

def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, "onlinecourse/course_details_bootstrap.html", {
        "course": course, "lessons": course.lessons.all(),
        "questions": course.questions.prefetch_related("choices").all()
    })

@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method != "POST":
        return redirect("course_details", course_id=course.id)
    questions = course.questions.prefetch_related("choices").all()
    score, total = 0, questions.count()
    for question in questions:
        choice_id = request.POST.get(f"question_{question.id}")
        if choice_id and question.choices.filter(pk=choice_id, is_correct=True).exists():
            score += question.grade
    submission = Submission.objects.create(student=request.user, course=course, score=score, total_questions=total)
    return redirect("show_exam_result", submission_id=submission.id)

@login_required
def show_exam_result(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id, student=request.user)
    return render(request, "onlinecourse/exam_result.html", {"submission": submission})
