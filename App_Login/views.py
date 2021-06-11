from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from App_Login.forms import TeacherSignUpForm, StudentSignUpForm, UserProfileChange, TeacherProfilePic, StudentProfilePic


def signup_teacher(request):
    form = TeacherSignUpForm()
    registered = False
    if request.method == 'POST':
        form = TeacherSignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            registered = True

    dict = {'form': form, 'registered': registered}
    return render(request, 'App_login/signup.html', context=dict)


def signup_student(request):
    form = StudentSignUpForm()
    registered = False
    if request.method == 'POST':
        form = StudentSignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            registered = True

    dict = {'form': form, 'registered': registered}
    return render(request, 'App_login/signup.html', context=dict)


def login_page(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

    return render(request, 'App_Login/login.html', context={'form': form})


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def profile(request):
    # print(request.user)
    return render(request, 'App_Login/profile.html', context={})


@login_required
def user_change(request):
    current_user = request.user
    form = UserProfileChange(instance=current_user)
    if request.method == 'POST':
        form = UserProfileChange(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            form = UserProfileChange(instance=current_user)
            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request, 'App_Login/change_profile.html', context={'form': form})


@login_required
def pass_change(request):
    current_user = request.user
    changed = False
    form = PasswordChangeForm(current_user)
    if request.method == 'POST':
        form = PasswordChangeForm(current_user, data=request.POST)
        if form.is_valid():
            form.save()
            changed = True
    return render(request, 'App_Login/change_pass.html', context={'form': form, 'changed': changed})


@login_required
def add_pro_pic(request):

    if request.user.is_teacher == True:
        form = TeacherProfilePic()
    else:
        form = StudentProfilePic()
        print("inside checking", request.user.is_student)

    # form = StudentProfilePic()

    if request.method == 'POST':
        if request.user.is_teacher == True:

            form = TeacherProfilePic(request.POST, request.FILES)
        else:
            form = StudentProfilePic(request.POST, request.FILES)
            print("inside post", request.user.is_student)

        # form = StudentProfilePic(request.POST, request.FILES)

        if form.is_valid():

            user_obj = form.save(commit=False)

            user_obj.user = request.user

            print("object user name", user_obj.user)
            print("user pic file name", user_obj.profile_pic)
            user_obj.save()
            print(request.user)
            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request, 'App_Login/pro_pic_add.html', context={'form': form})


@login_required
def change_pro_pic(request):

    print(request.user.is_student)

    if request.user.is_teacher == True:
        form = TeacherProfilePic(instance=request.user.teacher_user)
    else:
        form = StudentProfilePic(instance=request.user.student_user)

    if request.method == 'POST':

        if request.user.is_teacher == True:
            form = TeacherProfilePic(
                request.POST, request.FILES, instance=request.user.teacher_user)
        else:
            form = StudentProfilePic(
                request.POST, request.FILES, instance=request.user.student_user)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request, 'App_Login/pro_pic_add.html', context={'form': form})
