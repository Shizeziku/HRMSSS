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






# import logging
from django.contrib import messages





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


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Task, TaskAssignment,Employe_User
from .forms import TaskForm, TaskAssignmentForm
from django.contrib.auth.models import User
from django.utils import timezone
 



from collections import Counter
import json

def task_list(request):
    user = request.user
    print(f"user dashboard successfull redirect {user}")

    tasks = Task.objects.all()
    assigned_tasks = TaskAssignment.objects.all()

    # Count task priorities for the pie chart
    priority_counts = Counter(task.task_priority for task in tasks)

    return render(request, 'task_list.html', {
        'tasks': tasks,
        'assigned_tasks': assigned_tasks,
        'priority_counts': json.dumps(priority_counts)  # Convert to JSON for Chart.js
    })




def task_create(request):
    """Create a new task."""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            print("✅ New Task Created:", task.task_id)  # Debugging Task ID
            return redirect('task_list')
        else:
            print("❌ Form Errors:", form.errors)  # Debugging Form Errors
    else:
        form = TaskForm()

    return render(request, 'task_form.html', {'form': form})




def task_update(request, task_id):
    """Allows the admin to update a task."""
    task = get_object_or_404(Task, pk=task_id)

    if not request.user.is_staff:
        return redirect('task_list')

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')

    else:
        form = TaskForm(instance=task)
    
    return render(request, 'task_form.html', {'form': form})


@login_required
def task_delete(request, task_id):
    """Allows the admin to delete a task."""
    task = get_object_or_404(Task, pk=task_id)

    if not request.user.is_staff:
        return redirect('task_list')

    if request.method == "POST":
        task.delete()
        return redirect('task_list')

    return render(request, 'task_confirm_delete.html', {'task': task})




def assign_task(request):
    """View for assigning tasks to employees."""
    print(f"User: {request.user}, Superuser: {request.user.is_superuser}, Role: {getattr(request.user, 'role', 'No role')} - Trying to assign a task")


    if request.method == "POST":
        print("Received POST request for task assignment")
        form = TaskAssignmentForm(request.POST)
        if form.is_valid():
            task_assignment = form.save(commit=False)

            if request.user.is_superuser:
                task_assignment.assigned_by = None  # Set NULL since admin is not in Employe_User
                task_assignment.assigned_by_name = request.user.username  # Store admin's username
                print(f"Task assigned by Admin: {request.user.username}")
            else:
                try:
                    employe_user = Employe_User.objects.get(username=request.user.username)
                    task_assignment.assigned_by = employe_user
                    task_assignment.assigned_by_name = f"{employe_user.first_name} {employe_user.last_name}"
                    print(f"Task assigned by Employee: {task_assignment.assigned_by_name}")
                except Employe_User.DoesNotExist:
                    print("Error: No matching Employe_User found for this user.")
                    return redirect("task_list")

            task_assignment.save()
            print("Task assigned successfully!")
            return redirect("task_list")  # Redirect to task list page
        else:
            print("Form validation failed.")
    else:
        print("Rendering empty task assignment form.")
        form = TaskAssignmentForm()

    return render(request, "task_assign.html", {"form": form})




#####################3333
from django.shortcuts import render, redirect, get_object_or_404
from .models import PerformanceReview
from .forms import PerformanceReviewForm

def performance_reviews(request):
    """Fetch performance reviews based on user role."""
    user = request.user  # Logged-in user

    if user.is_superuser:  
        # Admin: See reviews where reviewed_by is also an admin
        reviews = PerformanceReview.objects.filter(reviewed_by__is_superuser=True)
    elif user.is_staff:  
        # Manager/Staff: See reviews where they are the reviewer
        reviews = PerformanceReview.objects.filter(reviewed_by=user)
    else:  
        # Regular Employee: See reviews where they are the employee
        reviews = PerformanceReview.objects.filter(employee=user)

    return render(request, 'review_list.html', {'reviews': reviews})

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PerformanceReviewForm

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PerformanceReviewForm

def add_review(request):
    """View for adding a new performance review."""
    print("➡️ Entering add_review view")  # Debugging

    if request.method == 'POST':
        print("📌 POST request received")  # Debugging

        form = PerformanceReviewForm(request.POST, user=request.user)
        print(f"🔍 Form initialized with data: {request.POST}")  # Debugging

        if form.is_valid():
            print("✅ Form is valid! Proceeding to save.")  # Debugging

            review = form.save(commit=False)  # Do not save to DB yet
            review.reviewed_by = request.user  # Assign the logged-in user
            review.save()  # Now save to DB

            messages.success(request, "Performance review added successfully!")
            print("💾 Review saved successfully!")  # Debugging

            return redirect('review_list')
        else:
            print("❌ Form submission failed. Errors below:")  # Debugging
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"  🔴 Field '{field}': {error}")  # Print each error

            messages.error(request, "Form submission failed. Please check errors below.")
    
    else:
        print("🟢 GET request received. Displaying empty form.")  # Debugging
        form = PerformanceReviewForm(user=request.user)

    return render(request, 'add_review.html', {'form': form})

def edit_review(request, review_id):
    review = get_object_or_404(PerformanceReview, pk=review_id)
    if request.method == 'POST':
        form = PerformanceReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('review_list')
    else:
        form = PerformanceReviewForm(instance=review)
    return render(request, 'edit_review.html', {'form': form, 'review': review})

def delete_review(request, review_id):
    review = get_object_or_404(PerformanceReview, pk=review_id)
    review.delete()
    return redirect('review_list')
####################################

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Leave, LeaveQuota
from .forms import LeaveApplicationForm, LeaveApprovalForm
from .models import Employe_User
@login_required
def apply_leave(request):
    if request.method == "POST":
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user  # Assign logged-in employee

            # Check if start_date or end_date is missing
            if not leave.start_date or not leave.end_date:
                form.add_error(None, "Start Date and End Date cannot be empty.")
                return render(request, 'apply_leave.html', {'form': form})  

            if leave.start_date > leave.end_date:
                form.add_error("start_date", "Start date cannot be after end date.")
                return render(request, 'apply_leave.html', {'form': form})  

            leave.save()
            return redirect('leave_status')

    else:
        form = LeaveApplicationForm()
    return render(request, 'apply_leave.html', {'form': form})

@login_required
def leave_status(request):
    """Displays the leave status for the logged-in employee."""
    leaves = Leave.objects.filter(employee=request.user)
    return render(request, 'leave_status.html', {'leaves': leaves})

@login_required
def approve_leave(request, leave_id):
    """Allows the admin to approve or reject leave requests."""
    leave = get_object_or_404(Leave, id=leave_id)

    if request.method == "POST":
        form = LeaveApprovalForm(request.POST, instance=leave)
        if form.is_valid():
            approved_leave = form.save(commit=False)
            approved_leave.approved_by = request.user  # Admin approving

            if approved_leave.status == 'approved':
                try:
                    quota = LeaveQuota.objects.get(employee=approved_leave.employee, leave_type=approved_leave.leave_type)
                    if approved_leave.total_days > quota.remain_quota:
                        messages.error(request, "Not enough leave balance.")
                    else:
                        quota.used_quota += approved_leave.total_days
                        quota.remain_quota -= approved_leave.total_days
                        quota.save()
                        approved_leave.save()
                        messages.success(request, "Leave approved successfully!")
                except LeaveQuota.DoesNotExist:
                    messages.error(request, "Leave quota not set.")
            else:
                approved_leave.save()
                messages.info(request, "Leave request rejected.")

            return redirect('admin_dashboard')

    else:
        form = LeaveApprovalForm(instance=leave)

    return render(request, 'approve_leave.html', {'form': form, 'leave': leave})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Leave

@login_required
def employee_leave_data(request):
    """View for admins to see all employee leave data"""
    if not request.user.is_staff:  # Ensure only admins can access
        return render(request, 'access_denied.html')

    leaves = Leave.objects.select_related('employee').all()
    
    return render(request, 'employee_leave_data.html', {'leaves': leaves})
