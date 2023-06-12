from django.shortcuts import render
from .threads import *
from .models import *


def homePage(request):
    return render(request, "index.html")