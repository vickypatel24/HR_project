from django.urls import path, re_path
from . import views, email_send

urlpatterns = [
    path('members/', views.members, name='members'),
    path('members1/', views.members1, name='members1'),
    path('add_dep/', views.add_dep, name='add_dep'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('edit_emp/<int:id>/', views.edit_emp, name='edit_emp'),
    path('delete_emp/<int:id>/', views.delete_emp, name='delete_emp'),
    path('edit_dep/<int:id>/', views.edit_dep, name='edit_dep'),
    path('delete_dep/<int:id>/', views.delete_dep, name='delete_dep'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('emp_list/', views.emp_list, name='emp_list'),
    path('dep_list/', views.dep_list, name='dep_list'),
    path('user_view/', views.user_view, name='user_view'),
    path('change_password/', views.change_password, name='change_password'),
    path('mail_view/', views.mail_view, name='mail_view'),
    path('Forgot_password/', views.forgot_password, name='Forgot_password'),
    path('verify_otp/<int:user_id>/', views.verify_otp, name='verify_otp'),
    path('reset_password/<int:user_id>/', views.reset_password, name='reset_password'),
    path('master/', views.master, name='master'),
    path('add_user/', views.add_user, name='add_user'),
    path('edit_user/', views.edit_user, name='edit_user'),

]