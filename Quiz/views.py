from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, ListView, DetailView, View, TemplateView, DeleteView
from Quiz.models import QuizName, Question
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from Quiz.forms import QuizForm, QuizQuestion, QuizTest
from django.http import JsonResponse

# Create your views here.


# @login_required
# def Quiz_Form(request):
#     form = QuizForm()
#     if request.method == 'POST':
#         form = QuizForm(request.POST)

#         if form.is_valid():
#             form.save(commit=False)
#             form.author_id = request.user
#             print(request.user)
#             form.save()
#             return HttpResponseRedirect(reverse('index'))

#     diction = {'title': "Add Quiz Name", 'form': form}
#     return render(request, 'Quiz/Quiz_form.html', context=diction)

class Quiz_Form(LoginRequiredMixin, CreateView):
    context_object_name = 'quiz'
    model = QuizName
    template_name = 'Quiz/Quiz_form.html'
    fields = ('quizname',)

    def form_valid(self, form):
        form_obj = form.save(commit=False)
        form_obj.author = self.request.user
        form_obj.save()
        return HttpResponseRedirect(reverse('Quiz:MyQuizzes'))


class MyQuizzes(LoginRequiredMixin, TemplateView):
    context_object_name = 'quiz'
    template_name = 'Quiz/my_quizzes.html'


class QuizList(ListView):
    context_object_name = 'quiz'
    model = QuizName
    template_name = 'Quiz/quiz_list.html'


@login_required
def quiz_details(request, pk):
    quiz_name = QuizName.objects.get(pk=pk)
    form = QuizQuestion()
    if request.method == 'POST':
        form = QuizQuestion(request.POST)
        if form.is_valid():
            form = form.save(commit=False)

            form.quiz = quiz_name
            form.save()
            return HttpResponseRedirect(reverse('Quiz:quiz_details', kwargs={'pk': pk}))
    return render(request, 'Quiz/Quiz_details.html', context={'quiz_name': quiz_name, 'form': form})


@login_required
def delete_quiz(request, pk):
    artist = QuizName.objects.get(pk=pk).delete()
    diction = {'delete_success': 'Quiz Deleted Successfully!'}
    return render(request, 'Quiz/delete.html', context=diction)


@login_required
def delete_question(request, pk):
    questiont = Question.objects.get(pk=pk).delete()
    diction = {'delete_success': 'Quiz Deleted Successfully!'}
    return render(request, 'Quiz/delete.html', context=diction)


@login_required
def edit_question(request, pk):
    question = Question.objects.get(pk=pk)
    form = QuizQuestion(instance=question)
    diction = {'form': form}
    if request.method == 'POST':
        form = QuizQuestion(request.POST, instance=question)

        if form.is_valid():
            form.save(commit=True)
            diction.update({'success_text': 'Successfully Updated!'})

    diction.update({'form': form})
    diction.update({'question_pk': pk})
    diction.update({'question': question})

    return render(request, 'Quiz/edit_question.html', context=diction)


@login_required
def test(request, pk):
    quiz_name = QuizName.objects.get(pk=pk)
    questions_list = Question.objects.filter(quiz=quiz_name)
    # print(questions)
    questions = []
    for question in questions_list:
        # print(question)
        # print(question.answer_1)
        # print(question.answer_2)
        # print(question.answer_3)
        # print(question.answer_4)
        # print(question.correct_answer)
        questions.append({str(question.question): [
                         question.answer_1, question.answer_2, question.answer_3, question.answer_4, question.correct_answer]})
    # print(questions[0])

    # if request.method == 'POST':
    #     data = request.POST['1']
    #     print("test data", data)

    return render(request, 'Quiz/test.html', context={'quiz_name': quiz_name, 'data': questions})


def listToString(s):

    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

    # return string
    return str1


@login_required
def save_quiz_view(request, pk):

    if request.is_ajax():
        questions = []
        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')

        user = request.user
        quiz_name = QuizName.objects.get(pk=pk)
        questions_list = Question.objects.filter(quiz=quiz_name)
        answer_list = []
        for answer in questions_list:
            answer_list.append(answer.correct_answer)
        attempted_ans = []
        for answer in data_.values():
            attempted_ans.append(listToString(answer))

        # converting string to integer
        for i in range(0, len(attempted_ans)):
            if attempted_ans[i] == '':
                attempted_ans[i] = 0
            else:
                attempted_ans[i] = int(attempted_ans[i])

        score = 0
        results = []
        correct_ans = None
        print("Attempted Quiz", data_)
        # print(questions_list)
        print("Actual Answer: ", answer_list)
        print("attempted answer: ", attempted_ans)

        for i in range(0, len(answer_list)):
            if attempted_ans[i] == 0:
                results.append(f"Question no {i+1} is not answered!!")
            elif answer_list[i] == attempted_ans[i]:
                score += 1
                results.append(f"Answer of the question-{i+1}  is correct")
            else:
                results.append(f"Answer of the question-{i+1} is wrong!")
        total_question = len(answer_list)
        score2 = f"{score} out of {total_question} answers are correct"
        percentage = f"{(score/total_question)*100}%"

        passed = False
        if float(score/total_question) >= 0.6:
            passed = True

    return JsonResponse({"Results": results, "Score": str(score), "Score2": str(score2), "Percentage_Score": percentage, "passed": passed, })
    # return render(request, 'Quiz/result.html', context={"Results: ": results, "Score: ": str(score), "score2": score2, "Percentage_Score: ": percentage})
