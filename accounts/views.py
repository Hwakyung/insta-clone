from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UserChangeForm,PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash 
from .models import User
from .forms import CustomUserCreationForm,CustomUserChangeForm
# Create your views here.
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('posts:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)

def logout(request):
    auth_logout(request)
    return redirect("accounts:login")

def user_page(req, id):
    #user라 이름을 변수로 설정하면 기존의 장고의 기능과 충돌할 가능성이 있음
    user_info = get_object_or_404(User, id=id)
    context ={
        'user_info':user_info
    }
    return render(req,'accounts/user_page.html',context)

def follow(req,id):
    you = get_object_or_404(User, id=id) #내가 팔로우할려고 하는 사람 
    me = req.user #지금 로그인하는 사람  
    if you != me : #자기 페이지인지 확인
        if me in you.followers.all() :
            me.followings.remove(you)
            # you.followers.remove(me)
        else:
            me.followings.add(you)
            # you.followers.add(me)

    return redirect('accounts:user_page',id)


def delete(req,id):
    user_info = get_object_or_404(User, id=id)
    user = req.user
    if req.method == "POST":
        if user == user_info :
            user.delete()
    else:
        pass
    return redirect('posts:index')

def update(req):
    if req.method == "POST":
        form = CustomUserChangeForm(req.POST,instance=req.user) #사용자가 수정할려는 최신 정보와 어느 정보를 수정할지를 확인
        if form.is_valid():
            form.save()
            return redirect('posts:index')
    else:
        form = CustomUserChangeForm(instance=req.user)
    context = {
        'form':form
    }
    return render(req,'accounts/form.html',context)


def password(req):
    if req.method == "POST":
        form = PasswordChangeForm(req.user, req.POST) #로그인한 사람의 정보와 post방식 확인
        if form.is_valid():
            form.save()
            update_session_auth_hash(req, form.user) #자동으로 로그인을 유지한채로 해쉬변경 form에 넣었던 유저 정보를 내보냄
            return redirect('posts:index')
    else:
        form = PasswordChangeForm(req.user)
    context = {
        'form':form
    }
    return render(req, 'accounts/form.html',context)

def profile(req):
    #현재 로그인한 사람의 정보가 뜸
    user_info = req.user
    context ={
        'user_info':user_info
    }
    return render(req,'accounts/user_page.html',context)