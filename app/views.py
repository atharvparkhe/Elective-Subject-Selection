from django.shortcuts import render, redirect
from django.contrib import messages
from .threads import *
from .models import *

context = {}


def homePage(request):
    return render(request, "index.html")


def allSubjects(request):
    context["subjects"] = SubjectModel.objects.all()
    return render(request, "subject/all-subjects.html", context=context)


def singleSubject(request, sub_id):
    try:
        if not SubjectModel.objects.filter(id=sub_id).exists():
            messages.error(request, 'Invalid Subject ID.')
            return redirect('all-subjects')
        context["subject"] = SubjectModel.objects.get(id=sub_id)
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "subject/single-subject.html", context=context)


