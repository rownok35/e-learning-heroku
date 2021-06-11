from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.db import transaction
from .models import User, Teacher, Student


class TeacherSignUpForm(UserCreationForm):
    email = forms.EmailField(label='Email Address', required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        teacher = Teacher.objects.create(user=user)

        teacher.save()
        return user


class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(label='Email Address', required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        student = Student.objects.create(user=user)

        student.save()
        return user


class UserProfileChange(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')


class TeacherProfilePic(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['profile_pic']


class StudentProfilePic(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['profile_pic']
