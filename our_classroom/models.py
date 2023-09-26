from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class Department(models.Model):
    dept_name = models.CharField(max_length=250, null=False, blank=False)
    head_of_dept = models.CharField(max_length=250, null=False, blank=False)

    def __str__(self):
        return self.dept_name


class AuthCode(models.Model):
    code = models.PositiveIntegerField(null=False, blank=False)
    used = models.BooleanField(default=False)


class Program(models.Model):
    program_name = models.CharField(max_length=250, null=False, blank=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.program_name


class Level(models.Model):
    level = models.PositiveBigIntegerField(null=False, blank=False)
    semester = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f"{self.level}({self.semester})"


class StudentClass(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    choices = (
        ("Morning", "Morning"),
        ("Evening", "Evening")
    )
    session = models.CharField(max_length=250, null=False, blank=False, choices=choices, default="Morning")
    activated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.program} L{self.level} {self.session}"


class Lecturer(models.Model):
    staff_id = models.CharField(max_length=200, unique=True, null=True, blank=True)
    name = models.CharField(max_length=250, null=False, blank=False)
    email = models.EmailField(blank=False, null=False)
    phone_number = models.PositiveBigIntegerField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    student_class = models.ManyToManyField(StudentClass, null=True, blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    course_name = models.CharField(max_length=250, null=False, blank=False)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    program_it_belongs_to = models.ForeignKey(Program, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    choices = (
        (1, "Monday"),
        (2, "Tuesday"),
        (3, "Wednesday"),
        (4, "Thursday"),
        (5, "Friday"),
        (6, "Saturday"),
        (7, "Sunday")
    )
    day_taught = models.CharField(choices=choices, max_length=200, null=True, blank=True)
    from_time = models.TimeField(auto_now_add=False, null=True, blank=True)
    to_time = models.TimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.course_name


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=200, blank=False, null=False)
    last_name = models.CharField(max_length=200, blank=False, null=False)
    username = models.CharField(max_length=200, null=False, blank=False, unique=True)
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE, null=True, blank=True)
    student_id = models.CharField(max_length=200, null=True, blank=True, unique=True)
    email = models.EmailField(null=True, blank=True)
    approved = models.BooleanField(default=False)
    choices = (
        ("Student", "Student"),
        ("Class Representative", "Class Representative")
    )
    role = models.CharField(max_length=200, null=False, blank=False, choices=choices, default="Student")
    phone_number = models.PositiveBigIntegerField(blank=True, null=True)
    password1 = models.CharField(max_length=100, null=False, blank=False)
    password2 = models.CharField(max_length=100, null=False, blank=False)
    status_choices = (
        ("Active", "Active"),
        ("Inactive", "Inactive")
    )
    status = models.CharField(max_length=100, null=False, blank=False, default="Active", choices=status_choices)

    def __str__(self):
        return self.first_name + "-" + self.username


class InformationCategory(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Information(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    category = models.ForeignKey(InformationCategory, on_delete=models.CASCADE)
    message = models.CharField(max_length=250, null=False, blank=False)
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.title


