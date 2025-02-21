from django.shortcuts import render,redirect,get_object_or_404
from .forms import Departmentform,userauthenticationForm,RegistrationForm,Rolesform,EmployeeForm
from .models import Department,Roles,Employe_User
from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from .auth_backend import custom_authenticate




# Create your views here.
def add(request):
    departments = Department.objects.filter(status=True)

    if request.method == 'POST':
        fm = Departmentform(request.POST)
        if fm.is_valid():
            dn=fm.cleaned_data['department_name']
            dd=fm.cleaned_data['department_description']
            reg = Department(department_name=dn,department_description=dd)
            reg.save()
            fm = Departmentform()  
    else:
        departments = Department.objects.filter(status=True)
        fm = Departmentform()   
        
    return render(request, 'add.html',{'form':fm, 'deprt':departments})

def home(request):
    return render(request,'home.html')
@login_required
def user_dashboard(request):
    user = request.user  # Fetch logged-in user
    user_role = user.role.role_name if user.role else "No Role Assigned"
    user_department = user.dept.department_name if user.dept else "No Department Assigned"

    context = {
        "user": user,
        "user_role": user_role,
        "user_department": user_department,
    }
    
    return render(request, "user_dashboard.html", context)

import datetime
Employe_User = get_user_model()  # Ensure Django uses your custom user model

def user_login(request):
    print("🔍 [DEBUG] Login View Called")  # Debug: View is accessed

    if request.method == "POST":
        print("🔍 [DEBUG] Received POST request")  # Debug: Check if POST request

        email = request.POST.get("email")
        password = request.POST.get("password")

        print(f"📩 [DEBUG] Email Entered: {email}")  # Debug: Print email input
        print(f"🔑 [DEBUG] Password Entered: {password}")  # Debug: Print password input (Avoid in production)

        if not email or not password:
            print("❌ [DEBUG] Missing Email or Password")  # Debug: Check for missing fields
            messages.error(request, "Email and password are required")
            return render(request, "login.html")

        user = custom_authenticate(email=email, password=password)
        
        print(f"🔍 [DEBUG] Authentication Function Returned: {user}")  # Debug: Print authentication result

        if user is not None:
            login(request, user)
            print(f"✅ [DEBUG] User Authenticated: {user.email}")  # Debug: Print authenticated email

            if user.is_superuser:
                print("🔄 [DEBUG] Redirecting Superuser to 'add' Page")
                return redirect("add")  # Redirect superusers
            else:
                print("🔄 [DEBUG] Redirecting Regular User to 'user_dashboard'")
                return redirect("user_dashboard")  # Redirect normal users
        else:
            print("❌ [DEBUG] Authentication Failed - Invalid Email or Password")  # Debug: Authentication failure
            messages.error(request, "Invalid email or password")

    print("🔍 [DEBUG] Rendering Login Page")  # Debug: If GET request or login failed
    return render(request, "login.html")


def logout_details(request):
    logout(request)
    return redirect('home')

def delete_product(request, id):
    deletedept = Department.objects.get(id=id)
    print('got', deletedept)
    deletedept.status = False
    deletedept.save()
    print() 
    fm = Departmentform()   
    return redirect('add')
 

def updateprod(request, id):
    # Safely get the department object or return a 404 if not found
    product = get_object_or_404(Department, id=id)
    
    if request.method == "POST":
        form = Departmentform(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('add')
        else:
            # Return the form with errors to the template
            return render(request, "update.html", {"form": form})
    else:
        # Initialize the form with the existing product instance
        form = Departmentform(instance=product)
        return render(request, "update.html", {"form": form})


def register(request):
    if request.method=="POST":
        RF=RegistrationForm(request.POST)
        if RF.is_valid():
            RF.save()
            return redirect('home')
        else:
            RF=RegistrationForm()
            return render(request,"register.html",{"RF":RF,'msg':'Worong credentials...!'})
    else:
        RF=RegistrationForm()
        return render(request,"register.html",{"RF":RF})


def roles(request):
    role = Roles.objects.filter(status=True)

    if request.method == 'POST':
        fm = Rolesform(request.POST)
        if fm.is_valid():
            dn=fm.cleaned_data['role_name']
            dd=fm.cleaned_data['role_description']
            reg = Roles(role_name=dn,role_description=dd)
            reg.save()
            fm = Rolesform()  
    else:
        role = Roles.objects.filter(status=True)
        fm = Rolesform()   
        
    return render(request, 'roles.html',{'form':fm, 'role':role})


def deleterole(request, id):
    deleterole = Roles.objects.get(id=id)
    print('got', deleterole)
    deleterole.status = False
    deleterole.save()
    print() 
    fm = Rolesform()   
    return redirect('roles')
 

def updaterole(request, id):
    # Safely get the department object or return a 404 if not found
    role = get_object_or_404(Roles, id=id)
    
    if request.method == "POST":
        form = Rolesform(request.POST, request.FILES, instance=role)
        if form.is_valid():
            form.save()
            return redirect('roles')
        else:
            # Return the form with errors to the template
            return render(request, "updaterole.html", {"form": form})
    else:
        # Initialize the form with the existing product instance
        form = Rolesform(instance=role)
        return render(request, "updaterole.html", {"form": form})




# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .models import EmployeeUser
# from .forms import EmployeeForm

# @login_required
# def employee_list(request):
    
#     employees = EmployeeUser.objects.all()

#     if request.method == 'POST':
#         form = EmployeeForm(request.POST)
#         if form.is_valid():
#             employee = form.save(commit=False)  
              
#             # Ensure reporting_manager is set to an EmployeeUser instance
#             if employee.reporting_manager and isinstance(employee.reporting_manager, EmployeeUser):
#                 employee.reporting_manager = employee.reporting_manager
#             else:
#                 employee.reporting_manager = None  # If invalid, default to None
            
#             employee.save()  # Save the employee instance
#             return redirect('employee_list')  # Redirect after successful submission
#     else:
#         form = EmployeeForm()

#     return render(request, 'employee_list.html', {'form': form, 'employees': employees})


# @login_required
# def employee_update(request, employee_id):
  
#     employee = get_object_or_404(EmployeeUser, pk=employee_id)

#     if request.method == 'POST':
#         form = EmployeeForm(request.POST, instance=employee)
#         if form.is_valid():
#             form.save()
#             return redirect('employee_list')
#     else:
#         form = EmployeeForm(instance=employee)

#     return render(request, 'employee_update.html', {'form': form, 'employee': employee})


# @login_required
# def employee_delete(request, employee_id):
#     employee = get_object_or_404(EmployeeUser, pk=employee_id)
#     if request.method == 'POST':
#         employee.delete()
#         return redirect('employee_list')

#     return render(request, 'employee_confirm_delete.html', {'employee': employee})


# import logging
from django.contrib import messages


# logger = logging.getLogger(__name__)

# def create_employee(request):
#     departments = Department.objects.filter(status=True)
#     roles = Roles.objects.filter(status=True)

#     if request.method == "POST":
#         form = EmployeeForm(request.POST)
#         if form.is_valid():
#             employee = form.save(commit=False)

#             # Get the department ID from the POST data
#             department_id = request.POST.get('dept')
#             # Adjust filtering based on the department ID or name
#             department = Department.objects.filter(id=department_id, status=True).first()

#             if not department:
#                 messages.error(request, "Invalid or inactive department selected")
#                 return render(request, 'employee_list.html', {'form': form, 'departments': departments, 'roles': roles})

#             # Get the role from the POST data
#             role_id = request.POST.get('role')
#             role = Roles.objects.filter(id=role_id, status=True).first()

#             if not role:
#                 messages.error(request, "Invalid or inactive role selected")
#                 return render(request, 'employee_list.html', {'form': form, 'departments': departments, 'roles': roles})

#             # Assign the department and role to the employee
#             employee.department = department
#             employee.role = role
#             employee.save()

#             messages.success(request, "Employee created successfully!")
#             return redirect('employee_list')

#     else:
#         form = EmployeeForm()

#     return render(request, 'employee_list.html', {'form': form, 'departments': departments, 'roles': roles})



from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EmployeeForm
from .models import Employe_User, Department, Roles

def create_employee(request):
    departments = Department.objects.filter(status=True)
    roles = Roles.objects.filter(status=True)
    employees = Employe_User.objects.all()  # ✅ Fetch all employees

    if request.method == "POST":
        print("🚀 Form Data Received:", request.POST)  # Debugging

        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)

            # Validate department
            department_id = request.POST.get('dept')
            department = Department.objects.filter(id=department_id, status=True).first()
            if not department:
                messages.error(request, "Invalid or inactive department selected")
                return render(request, 'employee_list.html', {
                    'form': form, 'departments': departments, 'roles': roles, 'employees': employees
                })

            # Validate role
            role_id = request.POST.get('role')
            role = Roles.objects.filter(id=role_id, status=True).first()
            if not role:
                messages.error(request, "Invalid or inactive role selected")
                return render(request, 'employee_list.html', {
                    'form': form, 'departments': departments, 'roles': roles, 'employees': employees
                })

            # Assign department and role
            employee.department = department
            employee.role = role
            employee.save()

            messages.success(request, "Employee created successfully!")
            return redirect('employee_list')

        else:
            messages.error(request, "Form is invalid. Please check the inputs.")
            print("⚠️ Form Errors:", form.errors)  # Debugging

    else:
        form = EmployeeForm()

    return render(request, 'employee_list.html', {
        'form': form, 'departments': departments, 'roles': roles, 'employees': employees
    })


def Forgot_pass(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = Employe_User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(f'/reset_password/{uidb64}/{token}/')           
            send_mail(
                'Password Reset',
                f'Click the following link to reset your password: {reset_url}',
                settings.EMAIL_HOST_USER, 
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Password reset link has been sent to your email.')
            return redirect('success_page')
        else:
            messages.success(request,'please enter valid email address')
    return render(request,"forgot_Password.html")

def success_page(request):
    return render(request, 'success.html')


def reset_password(request, uidb64, token):
    if request.method == 'POST':
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = Employe_User.objects.get(pk=uid)
                if default_token_generator.check_token(user, token):
                    user.set_password(password)
                    user.save()
                    return redirect('passwordresetdone')
                else:
                    return HttpResponse('Token is invalid', status=400)
            except (TypeError, ValueError, OverflowError, Employe_User.DoesNotExist):
                return HttpResponse('Invalid link', status=400)
        else:
            return HttpResponse('Passwords do not match', status=400)
    return render(request, 'reset_password.html')

def password_reset_done(request):
    return render(request, 'password_reset_done.html')