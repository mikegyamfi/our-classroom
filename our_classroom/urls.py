from django.urls import path
from . import views, authviews

urlpatterns = [
    path("", views.home, name='home'),

    path("sign-up/", authviews.sign_up, name="signup"),
    path("admin_registration", authviews.class_rep_sign_up, name='admin_reg'),
    path("login/", authviews.login_page, name="login"),
    path("logout/", authviews.logout_page, name="logout"),

    path('student_list', views.student_list, name='student_list'),
    path('course_list', views.course_list, name='course_list'),
    path('elevated/pending_approvals', views.unapproved_students, name='pending_approvals'),

    path('elevated/add_lecturer', views.add_lecturer, name='add_lecturer'),
    path('all_lecturers', views.all_lecturers, name='all_lecturers'),

    path('elevated/add_course', views.add_course, name='add_course'),
    path('elevated/send_class_info', views.send_class_info, name="send_class_info"),
    path('elevated/add_info_cat', views.info_category, name="add_info_cat"),
    path('elevated/approve_student/<int:pk>', views.approve_student, name='approve_student'),
    path('elevated/deny_student/<int:pk>', views.deny_student, name='deny_student')
]
