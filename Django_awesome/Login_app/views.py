from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView
from django.contrib.auth.models import User
from Login_app.models import userInfo
from Login_app.forms import userForm, userInfoForm, userInfoEditForm, userEditForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.


def index(request):
    dict = {'title': 'Home'}
    if request.user.is_authenticated:
        current_user = request.user
        user_id = current_user.id
        user_basic_info = User.objects.get(pk=user_id)
        user_more_info = userInfo.objects.get(user__pk=user_id)
        dict.update({'user_basic_info': user_basic_info})
        dict.update({'user_more_info': user_more_info})
    return render(request, 'Login_app/index.html', context=dict)

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = userForm(data=request.POST)
        user_info_form = userInfoForm(data=request.POST)

        if user_form.is_valid() and user_info_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            user_info = user_info_form.save(commit=False)
            user_info.user = user

            if 'profile_pic' in request.FILES:
                user_info.profile_pic = request.FILES['profile_pic']

            user_info.save()
            registered = True


    else:
        user_form = userForm()
        user_info_form = userInfoForm()

    dict = {'title': 'Register', 'userForm': user_form, 'userInfoForm': user_info_form, 'registered': registered}

    return render(request, 'Login_app/register.html', context=dict)


def logged_in(request):
    return render(request, 'Login_app/logged-in.html', context={})

def login_page(request):
    return render(request, 'Login_app/login.html', context={})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('Login_app:index'))
            else:
                return HttpResponse("User is not active")
        else:
            return HttpResponse("Username or password doesn't match!")
    else:
        return HttpResponseRedirect(reverse('Login_app:login'))

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Login_app:index'))

@login_required
def edit_profile(request):
    if request.user.is_authenticated:
        current_user = request.user
        user_id = current_user.id
        user_more = userInfo.objects.get(user__pk=user_id)
        user_basic = User.objects.get(pk=user_id)
        user_more_info = userInfoEditForm(instance=user_more)
        user_basic_info = userEditForm(instance=user_basic)
        if request.method == 'POST':
            user_more_info = userInfoEditForm(request.POST, instance=user_more)
            user_basic_info = userEditForm(request.POST, instance=user_basic)
            if user_more_info.is_valid() and user_basic_info.is_valid():
                user_more_info.save(commit=True)
                user_basic_info.save(commit=True)
                return HttpResponseRedirect(reverse('Login_app:index'))



    dict = {'user_more_info': user_more_info, 'user_basic_info': user_basic_info, 'user_id': user_id}
    return render(request, 'Login_app/edit-profile.html', context=dict)

class indexView(TemplateView):
    template_name = 'Login_app/test.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["text_1"] = "This is a sample text"
        return context
