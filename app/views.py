from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .threads import *
from .models import *

context = {}


def homePage(request):
    return render(request, "common/index.html")


def contactPage(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            msg = request.POST.get('message')
            thread_obj = send_contact_email(email, name)
            thread_obj.start()
            ContactUs.objects.create(name=name, email=email, msg=msg)
    except Exception as e:
        print(e)
    return render(request, "common/contact-us.html", context)


def timeTable(request):
    return render(request, "common/time-table.html")


def allSubjects(request):
    context["subjects"] = SubjectModel.objects.all()
    return render(request, "subject/all-subjects.html", context=context)


def singleSubject(request, sub_id):
    try:
        if not SubjectModel.objects.filter(id=sub_id).exists():
            messages.error(request, 'Invalid Subject ID.')
            return redirect('all-subjects')
        sub = SubjectModel.objects.get(id=sub_id)
        context["subject"] = sub
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "subject/single-subject.html", context=context)


@login_required(login_url="student-login")
def enroll(request, num):
    if num not in [1,2,3]:
        messages.error(request, "Invalid Subject Number")
        return redirect('student-dashboard')
    user = StudentModel.objects.get(email=request.user.email)
    if not EnollmentModel.objects.filter(student=user).exists():
        context["subjects"] = SubjectModel.objects.all()
    else:
        obj = EnollmentModel.objects.get(student=user)
        li = [obj.subject_1, obj.subject_2, obj.subject_3]
        context["subjects"] = SubjectModel.objects.all().exclude(li)
    return render(request, "common/time-table.html")


def changeElective(request, enrollment_id):
    return render(request, "common/time-table.html")



###############################################################################################################


@login_required(login_url="student-login")
def StudentDashboard(request):
    try:
        student_obj = StudentModel.objects.get(email=request.user.email)
        context["user"] = student_obj
        if not EnollmentModel.objects.filter(student=student_obj).exists():
            context["enrollment"] = None
        else :
            context["enrollment"] = EnollmentModel.objects.get(student=student_obj)
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "dashboard/student.html", context)


###############################################################################################################
