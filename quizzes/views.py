from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from courses.models import Course
from .models import Quiz, QuizAttempt, QuestionResult
from .forms import QuizForm, QuestionFormSet


@login_required(login_url="/users/login/")
def quiz_list_all(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quizzes/quiz_list.html', {
        "quizzes": quizzes,
        "course": None
    })


@login_required(login_url="/users/login/")
def quiz_list_by_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    quizzes = course.quizzes.all()

    return render(request, 'quizzes/quiz_list.html', {
        "quizzes": quizzes,
        "course": course
    })


@login_required(login_url="/users/login/")
def quiz_page(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    return render(request, 'quizzes/quiz_page.html', {
        'quiz': quiz,
        'questions': questions
    })


@login_required(login_url="/users/login/")
def quiz_new(request):
    if request.method == "POST":
        form = QuizForm(request.POST)
        formset = QuestionFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            quiz = form.save()
            formset.instance = quiz
            formset.save()
            return redirect('quizzes:list')
    else:
        form = QuizForm()
        formset = QuestionFormSet()

    return render(request, 'quizzes/quiz_new.html', {
        'form': form,
        'formset': formset
    })


@login_required(login_url="/users/login/")
def quiz_delete(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == "POST":
        quiz.delete()
        return redirect('quizzes:list')
    return redirect('quizzes:list')


@login_required(login_url="/users/login/")
def quiz_submit(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    # If someone tries to GET this URL, redirect safely
    if request.method != "POST":
        return redirect('quizzes:quiz-page', quiz_id=quiz.id)

    total_marks = sum(q.marks for q in questions)
    obtained_marks = 0

    # Create attempt record
    attempt = QuizAttempt.objects.create(
        user=request.user,
        quiz=quiz,
        total_marks=total_marks
    )

    results = []

    for question in questions:
        user_answer = request.POST.get(f"question_{question.id}", None)

        # Handle unanswered questions safely
        if user_answer is None:
            user_answer = "No answer selected"

        correct_answer = question.correct_answer
        is_correct = (user_answer == correct_answer)
        marks = question.marks if is_correct else 0

        if is_correct:
            obtained_marks += question.marks

        result = QuestionResult.objects.create(
            attempt=attempt,
            question=question,
            user_answer=user_answer,
            correct_answer=correct_answer,
            is_correct=is_correct,
            marks=marks
        )

        results.append(result)

    # Update attempt with final score
    attempt.obtained_marks = obtained_marks
    attempt.save()

    return render(request, "quizzes/quiz_results.html", {
        "quiz": quiz,
        "results": results,
        "obtained_marks": obtained_marks,
        "total_marks": total_marks,
        "user": request.user
    })

@login_required(login_url="/users/login/")
def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Get the latest attempt by this user
    attempt = QuizAttempt.objects.filter(
        user=request.user,
        quiz=quiz
    ).order_by('-timestamp').first()

    if not attempt:
        return render(request, "quizzes/quiz_results.html", {
            "quiz": quiz,
            "message": "You have not taken this quiz yet.",
            "results": [],
            "obtained_marks": 0,
            "total_marks": 0,
            "user": request.user
        })

    return render(request, "quizzes/quiz_results.html", {
        "quiz": quiz,
        "results": attempt.results.all(),
        "obtained_marks": attempt.obtained_marks,
        "total_marks": attempt.total_marks,
        "user": request.user
    })

@login_required(login_url="/users/login/")
def quiz_results_teacher(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Only teachers can view all student results
    if not request.user.isTeacher:
        return redirect('quizzes:quiz-results', quiz_id=quiz_id)

    # Get all attempts for this quiz
    attempts = QuizAttempt.objects.filter(quiz=quiz).select_related("user").order_by("-timestamp")

    return render(request, "quizzes/quiz_results_teacher.html", {
        "quiz": quiz,
        "attempts": attempts
    })
