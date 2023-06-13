from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from .threads import *
from .models import *
from .utils import *
import uuid

context = {}


def mailMessage(request):
    return render(request, "common/mail-message.html")


@login_required(login_url='index')
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
                messages.info(request, 'User does not exists.')
                return redirect('student-login')
            user = authenticate(email=email, password=password)
            if user is  None:
                messages.info(request, 'Incorrect Password.')
                return redirect('student-login')
            login(request, user)
            messages.success(request, 'Successfully logged in')
            return redirect('index')
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "auth/student/stu-login.html", context)


def StudentForgot(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            user = StudentModel.objects.get(email=email)
            if not user:
                messages.info(request, 'This user does not exist..')
                return redirect('student-login')
            token = str(uuid.uuid4())
            user.token = token
            thread_obj = send_forgot_link(email, token, "student")
            thread_obj.start()
            user.save()
            messages.info(request, 'We have sent you a link to reset password via mail')
            return redirect('mail-message')
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "auth/student/stu-forgot.html", context)


def StudentReset(request, token):
    try:
        student_obj = StudentModel.objects.get(token=token)
        if not student_obj:
            messages.info(request, 'This user does not exist..')
            return redirect('student-login')
        if request.method == 'POST':
            npw = request.POST.get('npw')
            cpw = request.POST.get('cpw')
            if npw == cpw:
                student_obj.set_password(cpw)
                student_obj.save()
                messages.info(request, 'Password Changed successfully.')
                return redirect('student-login')
            messages.error(request, 'New Password and Confirm Password dont match.')
            return redirect('student-login')
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "auth/student/stu-reset.html", context)


def TeacherLogIn(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            teacher_obj = TeacherModel.objects.filter(email=email).first()
            if teacher_obj is None:
                messages.info(request, 'User does not exists.')
                return redirect('teacher-login')
            user = authenticate(email=email, password=password)
            if user is  None:
                messages.info(request, 'Incorrect Password.')
                return redirect('teacher-login')
            login(request, user)
            messages.success(request, 'Successfully logged in')
            return redirect('index')
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "auth/teacher/tea-login.html", context)


def TeacherForgot(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            user = TeacherModel.objects.get(email=email)
            if not user:
                messages.info(request, 'This user does not exist..')
                return redirect('teacher-login')
            token = str(uuid.uuid4())
            user.token = token
            thread_obj = send_forgot_link(email, token, "teacher")
            thread_obj.start()
            user.save()
            messages.info(request, 'We have sent you a link to reset password via mail')
            return redirect('mail-message')
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "auth/teacher/tea-forgot.html", context)


def TeacherReset(request, token):
    try:
        teacher_obj = TeacherModel.objects.get(token=token)
        if not teacher_obj:
            messages.info(request, 'This user does not exist..')
            return redirect('teacher-login')
        if request.method == 'POST':
            npw = request.POST.get('npw')
            cpw = request.POST.get('cpw')
            if npw == cpw:
                teacher_obj.set_password(cpw)
                teacher_obj.save()
                messages.info(request, 'Password Changed successfully.')
                return redirect('teacher-login')
            messages.error(request, 'New Password and Confirm Password dont match.')
            return redirect('teacher-login')
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "auth/teacher/tea-reset.html", context)


def AdminLogIn(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            admin_obj = AdminModel.objects.filter(email=email).first()
            if admin_obj is None:
                messages.info(request, 'User does not exists.')
                return redirect('admin-login')
            user = authenticate(email=email, password=password)
            if user is  None:
                messages.info(request, 'Incorrect Password.')
                return redirect('admin-login')
            login(request, user)
            messages.success(request, 'Successfully logged in')
            return redirect('index')
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "auth/admin/admin-login.html", context)


def AdminForgot(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            admin_obj = AdminModel.objects.get(email=email)
            if not admin_obj:
                messages.info(request, 'This admin does not exist..')
                return redirect('admin-login')
            token = str(uuid.uuid4())
            admin_obj.token = token
            thread_obj = send_forgot_link(email, token, "student")
            thread_obj.start()
            admin_obj.save()
            messages.info(request, 'We have sent you a link to reset password via mail')
            return redirect('mail-message')
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "auth/admin/admin-forgot.html", context)


def AdminReset(request, token):
    try:
        admin_obj = AdminModel.objects.get(token=token)
        if not admin_obj:
            messages.info(request, 'This user does not exist..')
            return redirect('admin-login')
        if request.method == 'POST':
            npw = request.POST.get('npw')
            cpw = request.POST.get('cpw')
            if npw == cpw:
                admin_obj.set_password(cpw)
                admin_obj.save()
                messages.info(request, 'Password Changed successfully.')
                return redirect('admin-login')
            messages.error(request, 'New Password and Confirm Password dont match.')
            return redirect('admin-login')
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "auth/admin/admin-reset.html", context)


###############################################################################################################


@login_required(login_url="student-login")
def StudentDashboard(request):
    try:
        context["user"] = StudentModel.objects.get(email=request.user.email)
        context["abc"] = "abc"
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "dashboard/student.html", context)


###############################################################################################################


# @login_required("admin-login")
def allTeachers(request):
    context["teachers"] = TeacherModel.objects.all()
    return render(request, "teacher/all-teachers.html", context=context)


# @login_required("admin-login")
def singleTeacher(request, teacher_id):
    try:
        if not TeacherModel.objects.filter(id=teacher_id).exists():
            messages.error(request, 'Invalid Teacher ID.')
            return redirect('all-teachers')
        context["teacher"] = TeacherModel.objects.get(id=teacher_id)
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "teacher/single-teacher.html", context=context)


def addStudent(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('name')
            roll = request.POST.get('roll')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            if StudentModel.objects.filter(roll_no=roll).exists() or StudentModel.objects.filter(email=email).exists():
                messages.info(request, 'This account already exist')
                return redirect('add-student')
            obj = StudentModel.objects.create(name=name, email=email, phone=phone, roll_no=roll)
            pw = generate_random_passsword(12)
            obj.set_password(pw)
            obj.save()
            thread_obj = send_password_via_mail(email, pw)
            thread_obj.start()
            messages.info(request, 'Student Added')
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "students/add-single-student.html", context=context)

