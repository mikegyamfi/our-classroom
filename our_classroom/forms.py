from django import forms
from django.contrib.auth.forms import UserCreationForm

from our_classroom import models


class CustomUserForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(
        {'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'First Name', 'autofocus': True}))
    last_name = forms.CharField(
        widget=forms.TextInput(
            {'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Last Name'}))
    username = forms.CharField(
        widget=forms.TextInput(
            {'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Username'}))
    student_class = forms.ModelChoiceField(queryset=models.StudentClass.objects.filter(activated=True),
                                           empty_label=None,
                                           widget=forms.Select(
                                               {'class': 'form-control'}))
    student_id = forms.CharField(
        widget=forms.TextInput(
            {'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Student ID'}))
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    phone_number = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    def __init__(self, role, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if role == "Admin":
            self.fields['student_class'].queryset = models.StudentClass.objects.filter(activated=False).order_by('level')
        else:
            self.fields['student_class'].queryset = models.StudentClass.objects.filter(activated=True)

    class Meta:
        model = models.CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'student_id', 'student_class', 'password1',
                  'password2']


class Lecturer(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        {'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Jane Doe', 'autofocus': True}))
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'hello@example.com'}))
    phone_number = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0200000000'}))
    department = forms.ModelChoiceField(queryset=models.Department.objects.all(), empty_label=None, widget=forms.Select(
                                               {'class': 'form-control'}))

    class Meta:
        model = models.Lecturer
        fields = ['name', 'email', 'phone_number', 'department']


class EditLecturer(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        {'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Jane Doe', 'autofocus': True}))
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'hello@example.com'}))
    phone_number = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0200000000'}))
    department = forms.ModelChoiceField(queryset=models.Department.objects.all(), empty_label=None, widget=forms.Select(
                                               {'class': 'form-control'}))

    class Meta:
        model = models.Lecturer
        fields = ['name', 'email', 'phone_number', 'department']


class Course(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        {'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Course', 'autofocus': True}))
    course_code = forms.CharField(widget=forms.TextInput(
        {'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Course Code', 'autofocus': True}))
    lecturer = forms.ModelChoiceField(queryset=models.Lecturer.objects.all(), empty_label=None, widget=forms.Select(
                                               {'class': 'form-control'}))
    # program = forms.ModelChoiceField(queryset=models.Program.objects.all(), empty_label=None, widget=forms.Select(
    #                                            {'class': 'form-control'}))
    # level = forms.ModelChoiceField(queryset=models.Level.objects.all(), empty_label=None, widget=forms.Select(
    #                                            {'class': 'form-control'}))
    day = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=(
        (1, "Monday"), (2, "Tuesday"), (3, "Wednesday"), (4, "Thursday"), (5, "Friday"), (6, "Saturday"), (7, "Sunday")))
    from_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}))
    to_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}))


class EditCourse(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        {'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Course', 'autofocus': True}))
    lecturer = forms.ModelChoiceField(queryset=models.Lecturer.objects.all(), empty_label=None, widget=forms.Select(
                                               {'class': 'form-control'}))
    # program = forms.ModelChoiceField(queryset=models.Program.objects.all(), empty_label=None, widget=forms.Select(
    #                                            {'class': 'form-control'}))
    # level = forms.ModelChoiceField(queryset=models.Level.objects.all(), empty_label=None, widget=forms.Select(
    #                                            {'class': 'form-control'}))
    day = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=(
        (1, "Monday"), (2, "Tuesday"), (3, "Wednesday"), (4, "Thursday"), (5, "Friday"), (6, "Saturday"), (7, "Sunday")))
    from_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}))
    to_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}))


class InfoCategoryForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        {'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'E.g. Urgent, Important, Deadline', 'autofocus': True}))
    description = forms.CharField(widget=forms.Textarea(
        {'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Description', 'autofocus': True}))


class SendInfoForm(forms.Form):
    category = forms.ModelChoiceField(queryset=models.InformationCategory.objects.all(), empty_label=None, widget=forms.Select(
        {'class': 'form-control', 'autocomplete': 'off', 'autofocus': True}))
    title = forms.CharField(widget=forms.TextInput(
        {'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'E.g Class Rescheduled', 'autofocus': True}))
    message = forms.CharField(widget=forms.Textarea(
        {'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Detailed Message', 'autofocus': True}))

    def __init__(self, student_class, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = models.InformationCategory.objects.filter(student_class=student_class)








