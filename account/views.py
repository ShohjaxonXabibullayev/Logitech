from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from .forms import SignUpForm, LoginForm, ChangePassForm, ResetPassForm
from .utils import generate_code, send_to_mail


def logout_view(request):
    logout(request)
    messages.info(request, 'Siz dasturdan chiqdingiz')
    return redirect('home')

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Bu username orqali oldin royhatdan otilgan')
            else:
                form.save()
                messages.success(request, "Ro'yhatdan o'tdingiz")
                return redirect('login')
        else:
            messages.error(request, "Nimadir xatolik ketdi")
    form = SignUpForm()
    return render(request, 'account/signup.html', {'form':form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Siz dasturga kirdingiz")
            return redirect('home')
        else:
            messages.error(request, "Nimadir xato ketdi")
    form = LoginForm()
    return render(request, 'account/login.html', {'form':form})

def change_pass_view(request):
    if request.method == "GET":
        code = generate_code()
        request.session['verification_code'] = code
        send_to_mail(request.user.email, code)
        messages.info(request, 'Emailingizga kod yuborildi')
        form = ChangePassForm()

        return render(request, 'account/change_pass.html', {'form':form})
    else:
        form = ChangePassForm(request.POST)
        if form.is_valid():
            old_pass = form.cleaned_data['old_pass']
            new_pass = form.cleaned_data['new_pass']
            code = form.cleaned_data['code']
            session_code = request.session.get('verification_code')

            if not request.user.check_password(old_pass):
                messages.error(request, 'Parollar mos tushmayapti!')
                return redirect('change-pass')
            if session_code != code:
                messages.error(request, 'Tasdiqlash Codeingiz xato')
                return redirect('change-pass')

            user = request.user
            user.set_password(new_pass)
            user.save()
            messages.success(request, 'Parolingiz ozgartirldi')
            update_session_auth_hash(request, user)
            del request.session['verification_code']
            return redirect('profile')
        return redirect('change-pass')

from datetime import datetime, timedelta
def reset_pass(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            user = User.objects.get(username=username)
            code = generate_code()
            request.session['reset_code'] = code
            request.session['username'] = username
            request.session['create_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            send_to_mail(user.email, code)
            return redirect('reset2')
        except User.DoesNotExist:
            messages.error(request, 'Bunday foydalanuvchi mavjud emas')
            return render(request, 'account/reset_pass1.html')

    return render(request, 'account/reset_pass1.html')

def reset_pass2(request):
    if request.method == "POST":
        form = ResetPassForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            code = form.cleaned_data['code']
            session_code = request.session.get('reset_code')
            username = request.session.get('username')
            create_at = request.session.get('create_at')
            create_at = datetime.strptime(create_at, '%Y-%m-%d %H:%M:%S')

            if datetime.now() - create_at > timedelta(minutes=1):
                messages.info(request, 'Emailga yuborilgan kod eskirgan')
                return redirect('reset2')


            if session_code != code:
                messages.error(request, 'Tasdiqlash Codeingiz xato')
                return redirect('reset2')

            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            messages.success(request, 'Parolingiz ozgartirldi')
            del request.session['reset_code']
            del request.session['username']
            return redirect('login')
    return render(request, 'account/reset_pass2.html')



