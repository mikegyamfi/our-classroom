from time import sleep

import requests
from asgiref.sync import sync_to_async
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from our_classroom import models, forms, helper


# @login_required(login_url='login')
# Create your views here.
def home(request):
    user = models.CustomUser.objects.get(id=request.user.id)
    student_class = user.student_class
    courses = models.Course.objects.filter(level=user.student_class.level)
    all_info = models.Information.objects.filter(student_class=student_class)
    context = {'courses': courses, 'infos': all_info}
    return render(request, "layouts/index.html", context=context)


def student_list(request):
    user = models.CustomUser.objects.get(id=request.user.id)
    student_class = user.student_class
    all_students = models.CustomUser.objects.filter(student_class=student_class)
    context = {
        'students': all_students,
        'class': student_class
    }
    return render(request, "layouts/all_students.html", context=context)


def course_list(request):
    user = models.CustomUser.objects.get(id=request.user.id)
    student_class = user.student_class
    all_courses = models.Course.objects.filter(level=user.student_class.level)
    context = {
        'courses': all_courses,
        'class': student_class
    }
    return render(request, "layouts/all_courses.html", context=context)


def add_course(request):
    user = models.CustomUser.objects.get(id=request.user.id)
    student_class = user.student_class
    form = forms.Course()
    if user.role != "Class Representative":
        messages.warning(request, "Access Denied. Low Clearance Level.")
        return redirect("home")
    if request.method == "POST":
        form = forms.Course(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            lecturer = form.cleaned_data["lecturer"]
            day = form.cleaned_data["day"]
            from_time = form.cleaned_data["from_time"]
            to_time = form.cleaned_data["to_time"]
            program = student_class.program
            level = student_class.level

            if models.Course.objects.filter(course_name__contains=name):
                course = models.Course.objects.filter(course_name__contains=name)
                messages.success(request, f"Do you mean {course}?")
                return redirect('add_course')

            if models.Course.objects.filter(level=student_class.level, day_taught=day, from_time=from_time):
                course = models.Course.objects.filter(level=student_class.level, day_taught=day, from_time=from_time).first()
                messages.warning(request, f"A course already occupies that time. ({course})")
                return redirect('add_course')

            print(name)
            print(lecturer)
            print(day)
            print(from_time)
            print(to_time)

            new_course = models.Course.objects.create(
                course_name=name,
                lecturer=lecturer,
                program_it_belongs_to=program,
                level=level,
                day_taught=day,
                from_time=from_time,
                to_time=to_time
            )

            new_course.save()
            messages.success(request, "Course Added Successfully")
            return redirect('add_course')
    context = {
        'form': form,
        'class': student_class
    }
    return render(request, "layouts/add_course.html", context=context)


def unapproved_students(request):
    user = models.CustomUser.objects.get(id=request.user.id)
    student_class = user.student_class
    if user.role != "Class Representative":
        messages.warning(request, "Access Denied. Low Clearance Level.")
        return redirect("home")
    unapproved_students_list = models.CustomUser.objects.filter(approved=False, student_class=user.student_class)
    context = {'students': unapproved_students_list, 'class': student_class}
    return render(request, "layouts/pending_approvals.html", context=context)


def approve_student(request, pk):
    user = models.CustomUser.objects.get(id=request.user.id)
    student_class = user.student_class
    if user.role != "Class Representative":
        messages.warning(request, "Access Denied. Low Clearance Level.")
        return redirect("home")
    student_to_be_approved = models.CustomUser.objects.get(id=pk, student_class=student_class)
    name = student_to_be_approved.first_name + " " + student_to_be_approved.last_name
    phone = student_to_be_approved.phone_number
    print(phone)
    student_to_be_approved.approved = True
    student_to_be_approved.save()
    messages.success(request, f"{name} has been approved.")
    message = f"Hello {name}, Your account for the Classroom has been approved. You can log in now to join your classroom."
    url = f"https://sms.arkesel.com/sms/api?action=send-sms&api_key=cWhNWkhHcEV0SEZNTFpvT3B0V2o&to=233{phone}&from=Classroom&sms={message}"
    response = requests.get(url=url)
    print(response.json())
    return redirect('pending_approvals')


def deny_student(request, pk):
    user = models.CustomUser.objects.get(id=request.user.id)
    student_class = user.student_class
    if user.role != "Class Representative":
        messages.warning(request, "Access Denied. Low Clearance Level.")
        return redirect("home")
    student_to_be_approved = models.CustomUser.objects.get(id=pk, student_class=student_class)
    name = student_to_be_approved.first_name + " " + student_to_be_approved.last_name
    student_to_be_approved.approved = False
    messages.success(request, f"{name} has been denied.")
    return redirect('pending_approvals')


def add_lecturer(request):
    user = models.CustomUser.objects.get(id=request.user.id)
    student_class = user.student_class
    form = forms.Lecturer()
    if user.role != "Class Representative":
        messages.warning(request, "Access Denied. Low Clearance Level.")
        return redirect("home")
    if request.method == "POST":
        form = forms.Lecturer(request.POST)
        if form.is_valid():
            print("Sleeping")
            sleep(15)
            print("I slept")
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            phone_number = form.cleaned_data["phone_number"]
            department = form.cleaned_data["department"]
            staff_id = helper.staff_id_generator()

            print(name)
            print(email)
            print(phone_number)
            print(department)
            new_lecturer = models.Lecturer.objects.create(
                staff_id=staff_id,
                name=name,
                email=email,
                phone_number=phone_number,
                department=department,
            )
            new_lecturer.save()
            recent_lecturer_added = models.Lecturer.objects.get(name=name)
            recent_lecturer_added.student_class.add(student_class)
            recent_lecturer_added.save()
            messages.success(request, "Lecturer Added Successfully")
            return redirect('add_lecturer')
    context = {
        'class': student_class,
        'form': form
    }
    return render(request, "layouts/add_lecturer.html", context=context)


def all_lecturers(request):
    user = models.CustomUser.objects.get(id=request.user.id)
    student_class = user.student_class
    lecturers = models.Lecturer.objects.filter(student_class=student_class)
    context = {
        'lecturers': lecturers,
        'class': student_class
    }
    return render(request, "layouts/all_lecturers.html", context=context)


def send_class_info(request):
    user = models.CustomUser.objects.get(id=request.user.id)
    student_class = user.student_class
    form = forms.SendInfoForm(student_class=student_class)
    if request.method == "POST":
        form = forms.SendInfoForm(data=request.POST, student_class=student_class)
        if form.is_valid():
            category = form.cleaned_data["category"]
            title = form.cleaned_data["title"]
            message = form.cleaned_data["message"]

            new_info = models.Information.objects.create(
                category=category,
                title=title,
                student_class=student_class,
                message=message
            )
            new_info.save()
            messages.success(request, "Information Sent Successfully")
            return redirect('send_class_info')
    context = {
        'form': form,
        'class': student_class
    }
    return render(request, "layouts/info/send_info.html", context=context)


def info_category(request):
    user = models.CustomUser.objects.get(id=request.user.id)
    student_class = user.student_class
    form = forms.InfoCategoryForm()
    if request.method == "POST":
        form = forms.InfoCategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]

            new_info_cat = models.InformationCategory.objects.create(
                name=name,
                description=description,
                student_class=student_class
            )
            new_info_cat.save()
            messages.success(request, "Category Saved")
            return redirect("add_info_cat")
    context = {
        'class': student_class,
        'form': form
    }
    return render(request, "layouts/info/new_info_category.html", context=context)
