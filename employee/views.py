from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect

from .forms import EmployeeForm
from .models import Employee, Role, Department
from datetime import datetime
from django.db.models import Q


# Create your views here.


def index(request):
    return render(request, 'index.html')


def all_emp(request):
    emps = Employee.objects.all()
    # context = {
    #     'emps': emps
    # }
    return render(request, 'all_emp.html', {'emps': emps})


def remove_emp(request, id=0):
    if id:
        try:
            emp_to_be_removed = Employee.objects.get(id=id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee Removed Successfully")
        except:
            return HttpResponse("Please Enter A Valid EMP ID")
    emps = Employee.objects.all()

    return render(request, 'remove_emp.html', {'emps': emps})

def filter_emp(request):
    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        emps = Employee.objects.all()
        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept:
            emps = emps.filter(dept__name__icontains=dept)
        if role:
            emps = emps.filter(role__name__icontains=role)

        return render(request, 'all_emp.html', {'emps': emps})

    elif request.method == 'GET':
        return render(request, 'filter_emp.html')
    else:
        return HttpResponse('An Exception Occurred')


def msg(request):
    return render(request, 'msg.html')


def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        dept_id = int(request.POST['dept'])  # Get the department ID from the form
        role_id = int(request.POST['role'])  # Get the role ID from the form

        dept = Department.objects.get(id=dept_id)  # Retrieve the department object based on the ID
        role = Role.objects.get(id=role_id)  # Retrieve the role object based on the ID

        new_emp = Employee(
            first_name=first_name,
            last_name=last_name,
            salary=salary,
            bonus=bonus,
            phone=phone,
            dept=dept,  # Assign the department object to the employee
            role=role,  # Assign the role object to the employee
            hire_date=datetime.now()
        )
        new_emp.save()
        return HttpResponse('Employee Added Successfully....!')
    elif request.method == 'GET':
        departments = Department.objects.all()  # Retrieve all departments to pass to the template
        roles = Role.objects.all()  # Retrieve all roles to pass to the template
        return render(request, 'add_emp.html', {'departments': departments, 'roles': roles})
    else:
        return HttpResponse("An Exception Occurred! Employee Has Not Been Added")


def login(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['psswrd']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login()
            messages.info(request, 'user added')
        else:
            messages.error(request, ' not valid')

    return render(request, "login.html")


def register(request):
    if request.method == 'POST':
        uname = request.POST['username']
        email = request.POST['email']
        pword = request.POST['password']
        cpword = request.POST['confirm']

        if pword == cpword:
            if User.objects.filter(username=uname).exists():
                messages.info(request, 'Username already taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already taken')
                return redirect('register')
            else:
                User.objects.create_user(username=uname, password=pword, email=email)
                # Redirect to a success page or login page
                return redirect('/')  # Replace 'success' with the appropriate URL or view name

        else:
            messages.info(request, 'Passwords do not match')
            return redirect('register')

    return render(request, 'register.html')


def update_emp(request, id=0):
    if request.method == 'POST':
        emp = Employee.objects.get(id=id)
        form = EmployeeForm(request.POST, instance=emp)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        emp = Employee.objects.get(id=id)
        form = EmployeeForm(instance=emp)
        return render(request, 'update.html', {'form': form})