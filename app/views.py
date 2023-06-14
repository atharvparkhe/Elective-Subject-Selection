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
    return render(request, "common/contact.html", context)


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


def enroll(request, sub_id):
    return render(request, "common/time-table.html")
