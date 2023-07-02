from django.contrib.auth import logout
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.response import Response
from rest_framework import status
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
            ContactUs.objects.create(name=name, email=email, msg=msg)
            thread_obj = send_contact_email(email, name)
            thread_obj.start()
            messages.info(request, "Admin would contact you soon")
            return redirect("index")
    except Exception as e:
        print(e)
    return render(request, "common/contact-us.html", context)


def timeTable(request):
    return render(request, "common/time-table.html")


def allSubjects(request):
    context["subjects"] = SubjectModel.objects.all()
    return render(request, "subject/all-subjects.html", context=context)


@login_required(login_url="admin-login")
def adminAllSubjects(request):
    context["subjects"] = SubjectModel.objects.all()
    return render(request, "subject/all-subjects.html", context=context)


@login_required(login_url="admin-login")
def addSubject(request):
    try:
        context["departments"] = DepartmentModel.objects.all()
        context["faculty"] = TeacherModel.objects.all()
        if request.method == 'POST':
            SubjectModel.objects.create(
                name = request.POST.get('name'),
                desc = request.POST.get('desc'),
                cover_img = request.FILES['cover_img'],
                department = request.POST.get('dept'),
                teacher = request.POST.get('teacher'),
                syllabus = request.POST.get('syllabus'),
                intro = request.POST.get('intro')
            )
            messages.info(request, "Subject Added Successfully")
            return redirect("admin-dashboard")
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "subject/add-subject.html", context=context)


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
    try:
        if num not in ["1","2","3"]:
            messages.error(request, "Invalid Subject Number")
            return redirect('student-dashboard')
        user = StudentModel.objects.get(email=request.user.email)
        if not EnollmentModel.objects.filter(student=user).exists():
            context["subjects"] = SubjectModel.objects.all()
        else:
            obj = EnollmentModel.objects.get(student=user)
            li = [obj.subject_1.id]
            if obj.subject_2 != None:
                li.append(obj.subject_2.id)
            if obj.subject_3 != None:
                li.append(obj.subject_3.id)
            context["subjects"] = SubjectModel.objects.all().exclude(id__in=li)
        if request.method == 'POST':
            sub_id = request.POST.get('subject')
            if not SubjectModel.objects.filter(id=sub_id).exists():
                messages.error(request, "Invalid Subject ID")
                return redirect('student-dashboard')
            sub_obj = SubjectModel.objects.get(id=sub_id)
            if num == "1":
                obj.subject_1 = sub_obj
            elif num == "2":
                obj.subject_2 = sub_obj
            elif num == "3":
                obj.subject_3 = sub_obj
            obj.save()
            messages.info(request, "Elective Subject Added")
            return redirect('student-dashboard')
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "elective/enroll-form.html", context)


@login_required(login_url="student-login")
def changeElective(request, num):
    try:
        if num not in ["1","2","3"]:
            messages.error(request, "Invalid Subject Number")
            return redirect('student-dashboard')
        user = StudentModel.objects.get(email=request.user.email)
        obj = EnollmentModel.objects.get(student=user)
        li = [obj.subject_1.id]
        if num == "1":
            if obj.subject_2 != None:
                li.append(obj.subject_2.id)
            if obj.subject_3 != None:
                li.append(obj.subject_3.id)
        elif num == "2":
            li.append(obj.subject_2.id)
            if obj.subject_3 != None:
                li.append(obj.subject_3.id)
        elif num == "3":
            li.append(obj.subject_3.id)
            if obj.subject_2 != None:
                li.append(obj.subject_2.id)
        context["subjects"] = SubjectModel.objects.all().exclude(id__in=li)
        if request.method == 'POST':
            sub_id = request.POST.get('subject')
            if not SubjectModel.objects.filter(id=sub_id).exists():
                messages.error(request, "Invalid Subject ID")
                return redirect('student-dashboard')
            sub_obj = SubjectModel.objects.get(id=sub_id)
            email_list = [user.email, sub_obj.teacher.email]
            if num == "1":
                email_list.append(obj.subject_1.teacher.email)
                change_sub = obj.subject_1
            elif num == "2":
                email_list.append(obj.subject_2.teacher.email)
                change_sub = obj.subject_2
            elif num == "3":
                email_list.append(obj.subject_3.teacher.email)
                change_sub = obj.subject_3
            ChangeElectiveModel.objects.create(student=user, from_sub=change_sub, to_sub=sub_obj)
            thread_obj = send_subject_change_email(email_list)
            thread_obj.start()
            messages.info(request, "Elective Subject Change Requested")
            return redirect('student-dashboard')
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "elective/enroll-form.html", context)


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


@login_required(login_url="teacher-login")
def TeacherDashboard(request):
    try:
        if not TeacherModel.objects.filter(email=request.user.email):
            logout(request)
            return redirect("teacher-login")
        teacher_obj = TeacherModel.objects.get(email=request.user.email)
        context["teacher"] = teacher_obj
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "dashboard/teacher.html", context)


@login_required(login_url="admin-login")
def AdminDashboard(request):
    try:
        context["subject_count"] = SubjectModel.objects.all().count()
        context["teacher_count"] = TeacherModel.objects.all().count()
        context["student_count"] = StudentModel.objects.all().count()
        sub_names_array, sub_stu_count = [], []
        for sub in SubjectModel.objects.all():
            count = 0
            sub_names_array.append(sub.name)
            count = sub.enrolled_subject_1.all().count() + sub.enrolled_subject_2.all().count() + sub.enrolled_subject_3.all().count()
            sub_stu_count.append(count)
        context["subject"] = sub_names_array
        context["count"] = sub_stu_count
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "dashboard/admin.html", context)


@api_view(["GET"])
def get_graph_data(request):
    try:
        api_data = {}
        subject_name_array, dept_no_of_stu, dept_name_array, enrollment_count, change_count, to_change_count = [], [], [], [], [], []
        for sub in SubjectModel.objects.all():
            c1 = sub.enrolled_subject_1.all().count()
            c2 = sub.enrolled_subject_2.all().count()
            c3 = sub.enrolled_subject_3.all().count()
            subject_name_array.append(sub.name)
            enrollment_count.append(c1 + c2 + c3)
            change_count.append(sub.from_subject.all().count())
            to_change_count.append(sub.to_subject.all().count())
        for dept in DepartmentModel.objects.all():
            dept_name_array.append(dept.name)
            dept_no_of_stu.append(dept.student_department.all().count())
        api_data["subjects"] = subject_name_array
        api_data["depatments"] = dept_name_array
        api_data["dept_stu"] = dept_no_of_stu
        api_data["enrollments"] = enrollment_count
        api_data["change_from"] = change_count
        api_data["change_to"] = to_change_count
        return Response(api_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


###############################################################################################################

@login_required(login_url="teacher-login")
def enrolledStudentList(request):
    try:
        teacher_obj = TeacherModel.objects.get(email=request.user.email)
        subject_obj = teacher_obj.subject_teacher
        enrollments, students = [], []
        if subject_obj.enrolled_subject_1.all().count() != 0:
            enrollments.append(subject_obj.enrolled_subject_1.all())
        if subject_obj.enrolled_subject_2.all().count() != 0:
            enrollments.append(subject_obj.enrolled_subject_2.all())
        if subject_obj.enrolled_subject_3.all().count() != 0:
            enrollments.append(subject_obj.enrolled_subject_3.all())
        for enrr in enrollments:
            students.extend([stu.student for stu in enrr])
        context["students"] = students
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "students/all-students.html", context)


@login_required(login_url="teacher-login")
def studentProfile(request, stu_id):
    try:
        student_obj = StudentModel.objects.get(id=stu_id)
        context["user"] = student_obj
        if not EnollmentModel.objects.filter(student=student_obj).exists():
            context["enrollment"] = None
        else :
            context["enrollment"] = EnollmentModel.objects.get(student=student_obj)
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "dashboard/student.html", context)

