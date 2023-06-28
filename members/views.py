from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse, BadHeaderError, HttpResponseRedirect
from django.shortcuts import loader, redirect
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt
from django import forms
from random import randint, randrange

from .email_send import send_email
from .models import Employee, UserOtp
from .models import Dep


def members(request):
    template = loader.get_template('my_first.html')
    context = {
        'name': "Vitrag",
        'age': 25,
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url="/login/")
def members1(request):
    # print(request.user.first_name)
    name = request.user.first_name
    emp_list = Employee.objects.all()
    # print(emp_list)
    dep_list = Dep.objects.all().values()
    template = loader.get_template('my_first1.html')
    context = {
        'emp_list': emp_list,
        'dep_list': dep_list,
        'f_name': name
    }
    return HttpResponse(template.render(context, request))


class DepForm(forms.ModelForm):
    class Meta:
        model = Dep
        fields = "__all__"
        # exclude = ["dep_name", ""]


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"


# @csrf_exempt
def add_dep(request):
    name = request.user.first_name
    if not request.user.is_authenticated:
        return redirect('/login/')
    if request.POST:
        form = DepForm(request.POST)
        # dname = request.POST['dname']
        # dlocation = request.POST['dlocation']
        # dep = Dep(dep_name=dname, dep_location=dlocation)
        # dep.save()
        if form.is_valid():
            form.save()
            return redirect('/members1/')
    else:
        form = DepForm()

    template = loader.get_template('add_dep.html')
    context = {
        'form': form,
        'f_name': name
    }
    return HttpResponse(template.render(context, request))


def edit_dep(request, id):
    name = request.user.first_name

    if not request.user.is_authenticated:
        return redirect('/login/')
    dep_obj = Dep.objects.get(id=id)
    if request.POST:
        form = DepForm(request.POST, instance=dep_obj)
        # dname = request.POST['dname']
        # dlocation = request.POST['dlocation']
        # # dep = Dep(dep_name=dname, dep_location=dlocation)
        # dep_obj.dep_name= dname
        # dep_obj.dep_location= dlocation
        # dep_obj.save()
        # dep.save()
        if form.is_valid():
            form.save()
            return redirect('/members1/')
    else:
        form = DepForm(instance=dep_obj)

    template = loader.get_template('edit_dep.html')
    context = {
        'form': form,
        'f_name': name

    }
    return HttpResponse(template.render(context, request))


def delete_dep(request, id):
    name = request.user.first_name

    if not request.user.is_authenticated:
        return redirect('/login/')
    dep_obj = Dep.objects.get(id=id)
    if request.POST:
        dep_obj.delete()
        return redirect('/members1/')

    template = loader.get_template('delete_dep.html')
    context = {
        'dep_name': dep_obj.dep_name,
        'f_name': name

    }
    return HttpResponse(template.render(context, request))


def add_employee(request):
    name = request.user.first_name
    # print(request.user.is_authenticated)
    if not request.user.is_authenticated:
        return redirect('/login/')
    # u = request.user.is_authenticated
    # print(u)
    # dname_list = Dep.objects.all().values()
    # print(dname_list)
    # fname = request.POST['fname']
    # lname = request.POST['lname']
    # age = request.POST['age']
    # depid = request.POST['depid']
    # salary = request.POST['salary']
    # email = request.POST['email']
    # # try:
    # #     active = request.POST['active']
    # #     if active == "on":
    # #         active = True
    # # except Exception:
    # #     active = False
    # # print(active)
    # # if "active" in request.POST:
    # #     active = True
    # # else:
    # #     active = False
    # active = "active" in request.POST
    # # select * from dep where id = depid
    # dep = Dep.objects.get(id=depid)
    # emp = Employee(f_name=fname, l_name=lname, age=age, dep=dep, salary=salary, email=email, active=active)
    # # dep = Dep(dep_name=depname)
    # emp.save()
    if request.POST:
        form = EmployeeForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/members1/')
    else:
        form = EmployeeForm()

    template = loader.get_template('add_employee.html')
    context = {
        'form': form,
        'f_name': name

    }
    return HttpResponse(template.render(context, request))

@login_required(redirect_field_name="my_redirect_field", login_url='/login/')
def edit_emp(request, id):
    emp_obj = Employee.objects.get(id=id)
    name = request.user.first_name
    # dname_list = Dep.objects.all().values()

    if request.POST:
        form = EmployeeForm(request.POST, instance=emp_obj)
        # fname = request.POST['fname']
        # lname = request.POST['lname']
        # age = request.POST['age']
        # depid = request.POST['depid']
        # salary = request.POST['salary']
        # email = request.POST['email']
        # active = request.POST['active']
        # dep = Dep.objects.get(id=depid)
        # emp_obj.f_name = fname
        # emp_obj.l_name = lname
        # emp_obj.age = age
        # emp_obj.dep = dep
        # emp_obj.salary = salary
        # emp_obj.email = email
        # emp_obj.active = active
        # emp_obj.save()
        if form.is_valid():
            form.save()
            return redirect('/emp_list/')
    else:
        form = EmployeeForm(instance=emp_obj)

    template = loader.get_template('edit_emp.html')
    context = {
        # 'f_name': emp_obj.f_name,
        # 'l_name': emp_obj.l_name,
        # 'age': emp_obj.age,
        # 'depid': emp_obj.dep_id,
        # 'salary': emp_obj.salary,
        # 'email': emp_obj.email,
        # 'dname': dname_list,
        # 'active': emp_obj.active
        'form': form,
        'f_name': name

    }
    return HttpResponse(template.render(context, request))


def delete_emp(request, id):
    name = request.user.first_name
    if not request.user.is_authenticated:
        return redirect('/login/')
    emp_obj = Employee.objects.get(id=id)
    if request.POST:
        emp_obj.delete()
        return redirect('/members1/')

    template = loader.get_template('delete_emp.html')
    context = {
        'fu_name': emp_obj.f_name,
        'l_name': emp_obj.l_name,
        'f_name': name
    }
    return HttpResponse(template.render(context, request))


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    # else:
    #     return redirect('/login_view/')
    context = {
    }
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # print(username)
        # print(password)
        if user is not None:
            login(request, user)
            # print('okkk')
            next = request.GET.get('my_redirect_field')
            if next:
                return redirect(next)
            return redirect('/home/')

        else:
            context['error_msg'] = "Invalid User"
            print('error')
    template = loader.get_template('login_view.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url="/login/")
def change_password(request):
    name = request.user.first_name
    user_name = request.user.username
    print(user_name)

    if request.POST:
        n_pass = request.POST["n_password"]
        c_pass = request.POST["c_password"]
        print(n_pass)
        print(c_pass)

        if n_pass == c_pass:
            u = User.objects.get(username=user_name)
            u.set_password(n_pass)
            u.save()
            return redirect('/home/')

    template = loader.get_template('change_password.html')
    context = {
        'f_name': name,
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url="/login/")
def home(request):
    name = request.user.first_name
    template = loader.get_template('home_page.html')
    context = {
        'f_name': name
    }
    return HttpResponse(template.render(context, request))


def logout_view(request):
    # print("logout")
    logout(request)
    template = loader.get_template('log_out.html')
    context = {
    }
    return redirect('/login/')


@login_required(login_url="/login/")
def emp_list(request):
    name = request.user.first_name
    emp_list = Employee.objects.all()
    template = loader.get_template('emp_list.html')
    context = {
        'emp_list': emp_list,
        'f_name': name
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url="/login/")
def dep_list(request):
    name = request.user.first_name
    dep_list = Dep.objects.all().values()
    print(dep_list)
    template = loader.get_template('dep_list.html')
    context = {
        'dep_list': dep_list,
        'f_name': name
    }
    return HttpResponse(template.render(context, request))

def master(request):
    name = request.user.first_name
    template = loader.get_template('master.html')
    context = {
        'f_name': name
    }
    return HttpResponse(template.render(context, request))



@login_required(login_url="/login/")
def user_view(request):
    name = request.user.first_name
    # fname = request.user.first_name
    # lname = request.user.last_name
    # print(fname)
    # print(lname)
    user_list = User.objects.all().values()
    # print(user_list)
    template = loader.get_template('user_view.html')
    context = {
        # 'f_name': fname,
        # 'l_name': lname,
        'f_name': name,
        'user_list': user_list,
    }
    return HttpResponse(template.render(context, request))


def mail_view1(request, mail=None):
    # send_mail("test", "my message ", settings.EMAIL_HOST_USER, ["vitragtest@mailinator.com", ])
    # send_email("vitragtest@mailinator.com")
    mail_id = request.POST['subject']
    mail = request.POST['message']
    print(mail_id)
    print(mail)

    template = loader.get_template('mail_view.html')
    context = {

    }
    return HttpResponse(template.render(context, request))


def mail_view(request):
    template = loader.get_template('mail_view.html')
    context = {}

    if request.POST:
        # subject = request.POST.get('subject', '')
        # message = request.POST.get('message', '')
        to_email = request.POST.get('to_email', '')

        try:
            user = User.objects.get(email=to_email)
        except:
            print("Invalid")
            context['error_msg'] = "Invalid email"
        else:
            # print(subject)
            # print(message)
            print(to_email)
            subject = "Forgot Password Request"
            otp = randint(100000, 999999)
            message = f"Your otp is {otp}"
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [to_email])
                u_otp = UserOtp(user=user, otp=otp)
                u_otp.save()
                print(user.id)
            except BadHeaderError:
                context['error_msg'] = "Error in email send"
            return HttpResponseRedirect(f'/verify_otp/{user.id}/')
    return HttpResponse(template.render(context, request))


def forgot_password(request):
    template = loader.get_template('Forgot_password.html')
    context = {}

    if request.POST:
        e_mail = request.POST.get('e_mail', '')
        try:
            user = User.objects.get(email=e_mail)
            print(user)
        except:
            context['error_msg'] = "Invalid email"
        else:
            print(e_mail)
            subject = "Forgot Password Request"
            otp = randint(100000, 999999)
            message = f"Your otp is {otp}"
            print(message)
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [e_mail])
                UserOtp.objects.filter(user=user).delete()
                u_otp = UserOtp(user=user, otp=otp)
                u_otp.save()
                print(user.id)
            except BadHeaderError:
                context['error_msg'] = "Error in email send"
            return HttpResponseRedirect(f'/verify_otp/{user.id}/')
    return HttpResponse(template.render(context, request))


def verify_otp(request, user_id):
    template = loader.get_template('verify_otp.html')
    context = {}

    if request.POST:
        otp = request.POST.get('otp', '')
        if otp:
            try:
                u_otp = UserOtp.objects.get(otp=otp, user_id=user_id)
            except:
                context['error_msg'] = "Invalid OTP"
            else:
                u_otp.delete()
                return HttpResponseRedirect(f'/reset_password/{user_id}')
    return HttpResponse(template.render(context, request))



def reset_password(request, user_id):
    template = loader.get_template('reset_password.html')
    context = {}
    user_name = request.user.username
    print(user_name)

    if request.POST:
        n_pass = request.POST["n_password"]
        c_pass = request.POST["c_password"]
        print(n_pass)
        print(c_pass)

        if n_pass == c_pass:
            u = User.objects.get(id=user_id)
            print(u)
            u.set_password(n_pass)
            u.save()
            return redirect('/home/')
        else:
            context['error_msg'] = "Enter Same Password"


    return HttpResponse(template.render(context, request))

def add_user(request):
    template = loader.get_template('add_user.html')
    context = {}
    if request.POST:
        u = User.objects.all()
        username = request.POST["username"]
        f_name = request.POST["f_name"]
        l_name = request.POST["l_name"]
        e_mail = request.POST["e_mail"]
        password = request.POST["password"]
        n_pass = request.POST["c_password"]
        n_user = User(username=username, first_name=f_name, last_name=l_name, email=e_mail, password=password)
        n_user.save()
        # user = User.objects.all().values()
        # print(user)
        return redirect('/home/')


    return HttpResponse(template.render(context, request))

def edit_user(request):
    template = loader.get_template('edit_user.html')
    context = {
    }
    return HttpResponse(template.render(context, request))
