from django import forms
from django.db.models import fields
from django.forms.widgets import Select
from Quiz.models import QuizName, Question


class QuizForm(forms.ModelForm):
    class Meta:
        model = QuizName
        fields = ('quizname',)


class QuizQuestion(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ('quiz',)
    correct_answer = forms.CharField(

        widget=forms.TextInput(
            attrs={
                'placeholder': "Just enter the number of the answer. If 'answer 1' is correct then just write 1 "}
        )
    )


class QuizTest(forms.Form):
    def __init__(self, data, questions, *args, **kwargs):
        pass
    # answer1 = Question.answer_1
    # answer2 = Question.answer_2
    # answer3 = Question.answer_3
    # answer4 = Question.answer_4
    # choices = ((1, answer1), (2, answer2), (3, answer3), (4, answer4))
    # select = forms.ChoiceField(label=Question.question, required=True, choices=choices, widget=forms.RadioSelect)
