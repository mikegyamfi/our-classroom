from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from our_classroom import forms, models


def sign_up(request):
    if request.user.is_authenticated:
        messages.warning(request, "Log out to sign up for a different account.")
        return redirect('home')
    form = forms.CustomUserForm(role="User")
    if request.method == "POST":
        form = forms.CustomUserForm(data=request.POST, role="User")
        if form.is_valid():
            print(form.cleaned_data["student_id"])
            form.save()
            messages.info(request, f"Sign Up Successful. Log in to continue.")
            return redirect('login')
        else:
            print("nope")
    context = {'form': form}
    return render(request, "auth/register.html", context=context)


def class_rep_sign_up(request):
    if request.user.is_authenticated:
        messages.warning(request, "Log out to sign up for a different account.")
        return redirect('home')
    form = forms.CustomUserForm(role="Admin")
    if request.method == "POST":
        form = forms.CustomUserForm(data=request.POST, role="Admin")
        if form.is_valid():
            username = form.cleaned_data["username"]
            student_class = form.cleaned_data["student_class"]
            print(type(student_class))
            code = request.POST.get("code")
            code_needed = models.AuthCode.objects.filter(code=code, used=False).first()
            if code_needed:
                code_needed.used = True
                code_needed.save()
                form.save()
                user = models.CustomUser.objects.get(username=username)
                user.role = "Class Representative"
                user.approved = True
                user.save()
                class_to_be_activated = models.StudentClass.objects.get(id=student_class.id)
                class_to_be_activated.activated = True
                class_to_be_activated.save()
                messages.info(request, f"Sign Up Successful. Log in to continue.")
                return redirect('login')
            else:
                messages.error(request, "Invalid Authorization Code")
                return redirect('')
        else:
            print("nope")
    context = {'form': form}
    return render(request, "auth/class_rep_signup.html", context=context)


def login_page(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('home')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            password = request.POST.get('pass')

            print(name)
            print(password)

            user = authenticate(request, username=name, password=password)
            print(user)
            if user:
                if not user.approved:
                    messages.error(request, "You have not been approved yet by your Class Representative")
                    return redirect('login')
                login(request, user)
                messages.success(request, 'Log in Successful')
                return redirect('home')
            else:
                print("here")
                messages.info(request, 'Invalid username or password')
                return redirect('login')
    return render(request, "auth/login.html")


@login_required(login_url='login')
def logout_page(request):
    logout(request)
    messages.success(request, "Log out successful")
    return redirect('home')


