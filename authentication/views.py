from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from django.conf import settings
from .serializers import *
from .threads import *
from .models import *
from .utils import *
import uuid, pandas

context = {}


def mailMessage(request):
    return render(request, "common/mail-message.html")


@login_required(login_url='index')
def logoutView(request):
    logout(request)
    return redirect("index")


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
            return redirect('student-dashboard')
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
            return redirect('teacher-dashboard')
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


@api_view(["POST"])
def AddAdmin(request):
    try:
        data = request.data
        serializer = signupSerializer(data=data)
        if serializer.is_valid():
            name = serializer.data["name"]
            email = serializer.data["email"]
            password = serializer.data["password"]
            if AdminModel.objects.filter(email=email).first():
                return Response({"message":"Acount already exists."}, status=status.HTTP_406_NOT_ACCEPTABLE)
            new_admin = AdminModel.objects.create(
                email = email,
                name = name,
            )
            new_admin.set_password(password)
            new_admin.save()
            return Response({"message":"Account created"}, status=status.HTTP_201_CREATED)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



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
            return redirect('admin-dashboard')
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


def allTeachers(request):
    context["teachers"] = TeacherModel.objects.all()
    return render(request, "teacher/all-teachers.html", context=context)


@login_required(login_url="admin-login")
def adminAllTeachers(request):
    context["teachers"] = TeacherModel.objects.all()
    return render(request, "teacher/admin-all-teachers.html", context=context)


@login_required(login_url="admin-login")
def singleTeacher(request, teacher_id):
    try:
        if not TeacherModel.objects.filter(id=teacher_id).exists():
            messages.error(request, 'Invalid Teacher ID.')
            return redirect('all-teachers')
        context["teacher"] = TeacherModel.objects.get(id=teacher_id)
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "teacher/single-teacher.html", context=context)

@login_required(login_url="admin-login")
def adminSingleTeacher(request, teacher_id):
    try:
        if not TeacherModel.objects.filter(id=teacher_id).exists():
            messages.error(request, 'Invalid Teacher ID.')
            return redirect('all-teachers')
        context["teacher"] = TeacherModel.objects.get(id=teacher_id)
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "teacher/admin-single-teacher.html", context=context)


@login_required(login_url="admin-login")
def addStudent(request):
    try:
        context["departments"] = DepartmentModel.objects.all()
        if request.method == 'POST':
            name = request.POST.get('name')
            roll = request.POST.get('roll')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            if StudentModel.objects.filter(roll_no=roll).exists() or StudentModel.objects.filter(email=email).exists():
                messages.info(request, 'This account already exist')
                return redirect('add-student')
            obj = StudentModel.objects.create(name=name, email=email, phone=phone, roll_no=roll, department=DepartmentModel.objects.first())
            pw = generate_random_passsword(12)
            obj.set_password(pw)
            obj.save()
            thread_obj = send_password_via_mail(email, pw)
            thread_obj.start()
            messages.info(request, 'Student Added Successfully')
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "students/add-single-student.html", context=context)


@login_required(login_url="admin-login")
def addMultipleStudents(request):
    try:
        if request.method == 'POST':
            obj = FileModel.objects.create(file=request.FILES['excelfile'])
            obj.save()
            # file_path = f"{settings.BASE_DIR}/{obj.file}"
            df = pandas.read_excel(obj.file)
            for stu in df.values.tolist():
                obj = StudentModel.objects.create(
                    roll_no = stu[0],
                    name = stu[1],
                    email = stu[2],
                    phone = stu[3],
                    department = DepartmentModel.objects.get(code=stu[4])
                )
                pw = generate_random_passsword(12)
                obj.set_password(pw)
                obj.save()
                thread_obj = send_password_via_mail(stu[2], pw)
                thread_obj.start()
            messages.info(request, 'Students Added Successfully')
            return redirect("admin-dashboard")
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "students/add-multiple-students.html", context=context)


@login_required(login_url="admin-login")
def addTeacher(request):
    try:
        context["departments"] = DepartmentModel.objects.all()
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "teacher/add-teacher.html", context=context)


@login_required(login_url="admin-login")
def adminAllStudents(request):
    context["students"] = StudentModel.objects.all()
    return render(request, "students/admin-all-students.html", context)


@login_required(login_url="admin-login")
def adminSingleStudent(request, stu_id):
    try:
        if not StudentModel.objects.filter(id=stu_id).exists():
            messages.error(request, "Invalid Student ID")
            return redirect("all-students")
        student_obj = StudentModel.objects.get(id=stu_id)
        context["student"] = student_obj
        from app.models import EnollmentModel
        if not EnollmentModel.objects.filter(student=student_obj).exists():
            context["enrollment"] = None
        else :
            context["enrollment"] = EnollmentModel.objects.get(student=student_obj)
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "students/admin-single-student.html", context)
