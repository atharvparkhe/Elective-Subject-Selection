from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .threads import *
from .models import StudentModel
import uuid

context = {}

@login_required(login_url='login')
def logoutView(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def StudentLogIn(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            student_obj = StudentModel.objects.filter(email=email).first()
            if student_obj is None:
                messages.info(request, 'User does not exists. Please Signup')
                return redirect('student-login')
            user = authenticate(email=email, password=password)
            if user is  None:
                messages.info(request, 'Incorrect Password.')
                return redirect('student-login')
            login(request, user)
            messages.success(request, 'Successfully logged in')
            return redirect('index')
    except Exception as e:
        print(e)
        messages.error(request, str(e))
    return render(request, "student/auth/stu-login.html", context)


def StudentForgot(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            user = StudentModel.objects.get(email=email)
            if not user:
                messages.info(request, 'This user does not exist. Please Signup.')
                return redirect('student-login')
            token = str(uuid.uuid4())
            user.token = token
            thread_obj = send_forgot_link(email, token, "student")
            thread_obj.start()
            user.save()
            messages.info(request, 'We have sent you a link to reset password via mail')
            # return redirect('stu-message')
    except Exception as e:
        print(e)
        messages.error(request, str(e))
    return render(request, "student/auth/stu-forgot.html", context)


def StudentReset(request, token):
    try:
        student_obj = StudentModel.objects.get(token=token)
        if not student_obj:
            messages.info(request, 'This user does not exist. Please Signup.')
            return redirect('/signup')
        if request.method == 'POST':
            npw = request.POST.get('npw')
            cpw = request.POST.get('cpw')
            if npw == cpw:
                student_obj.set_password(cpw)
                student_obj.save()
                messages.info(request, 'Password Changed successfully.')
                return redirect('/login')
            messages.error(request, 'New Password and Confirm Password dont match.')
            return redirect('/login')
    except Exception as e :
        print(e)
        messages.error(request, str(e))
    return render(request, "student/accounts/reset.html", context)

