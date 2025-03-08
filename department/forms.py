from django import forms
from .models import Department,Roles,Employe_User
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm



class Departmentform(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name','department_description']
        widgets = {
            'department_name' : forms.TextInput(attrs={'class':'form-control'}),
            'department_description' : forms.TextInput(attrs={'class':'form-control'}),
        }

class userauthenticationForm (AuthenticationForm):
    username=forms.CharField(label="Enter username",widget=forms.TextInput(attrs={'class':'form-control'})),
    password=forms.CharField(label="Enter password",widget=forms.PasswordInput(attrs={'class':'form-control'})),   
    
    class Meta:
        model=User
        fields=['username','password']

from django import forms
from .models import Employe_User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    mobile = forms.CharField(
        max_length=100, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Employe_User  
        fields = ['username', 'first_name', 'last_name', 'email', 'mobile', 'password1', 'password2']
        
        labels = {
            'username': 'Enter Username',
            'first_name': 'Enter First Name',
            'last_name': 'Enter Last Name',
            'email': 'Enter Email',
            'mobile': 'Enter Mobile Number',
            'password1': 'Enter Password',
            'password2': 'Confirm Password',
        }
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if Employe_User.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError("This mobile number is already in use. Please enter a different one.")
        return mobile



class loginform(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password']
        
        labels={
            'username':'Enter Username',
            'password':'Enter password',
        }
        
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'}),
        }


class Rolesform(forms.ModelForm):
    class Meta:
        model = Roles
        fields = ['role_name','role_description']
        widgets = {
            'role_name' : forms.TextInput(attrs={'class':'form-control'}),
            'role_description' : forms.TextInput(attrs={'class':'form-control'}),
        }



class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employe_User
        fields = [
            'first_name','last_name','email','mobile','role','dept','reporting_manager', 
            'date_of_joining','username', 'password'
        ]
        
        widgets = {
            'password': forms.PasswordInput(),
            'date_of_joining': forms.DateInput(attrs={'type': 'date'}),
        }

    first_name = forms.CharField(max_length=100, required=True, label="First Name")
    last_name = forms.CharField(max_length=100, required=True, label="Last Name")
    email = forms.EmailField(max_length=100, required=True, label="Email")
    mobile = forms.CharField(max_length=100, required=True, label="Mobile Number")
    role = forms.ModelChoiceField(queryset=Roles.objects.all(), required=True, label="Select Role")
    dept = forms.ModelChoiceField(queryset=Department.objects.all(), required=True, label="Select Department")
    reporting_manager = forms.ModelChoiceField(
        queryset=Employe_User.objects.all(), required=False, label="Allocate Reporting Manager"
    )
    date_of_joining = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date of Joining")
    username = forms.CharField(max_length=100, required=True, label="Username")
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label="Set Password")



from django import forms
from .models import Task, TaskAssignment

class TaskForm(forms.ModelForm):
    """Form for creating and editing tasks."""
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'task_title': forms.TextInput(attrs={'class': 'form-control'}),
            'task_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'task_priority': forms.Select(attrs={'class': 'form-control'}),
            'task_type': forms.Select(attrs={'class': 'form-control'}),
        }

class TaskAssignmentForm(forms.ModelForm):
    """Form for assigning tasks to employees."""
    
    class Meta:
        model = TaskAssignment
        fields = ['task', 'employee']  # Removed 'status' from fields for admin
        widgets = {
            'task': forms.Select(attrs={'class': 'form-control'}),
            'employee': forms.Select(attrs={'class': 'form-control'}),
        }

#######################
from django import forms
from .models import PerformanceReview
from django.contrib.auth import get_user_model

User = get_user_model()  # Get the User model

class PerformanceReviewForm(forms.ModelForm):
    RATING_CHOICES = [(str(i), str(i)) for i in range(1, 11)]  # Generates choices from 1 to 10

    class Meta:
        model = PerformanceReview
        fields = ['review_title', 'employee', 'reviewed_by', 'review_period', 'rating', 'comments']
        widgets = {
            'review_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter review title'}),
            'employee': forms.Select(attrs={'class': 'form-select'}),
            'review_period': forms.Select(choices=[('Monthly', 'Monthly'), ('Quarterly', 'Quarterly'), ('Annual', 'Annual')],
                                          attrs={'class': 'form-select'}),
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter comments'}),
        }

    rating = forms.ChoiceField(
        choices=RATING_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-select'}), 
        label="Rating (1-10)"
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Fetch logged-in user
        super().__init__(*args, **kwargs)

        self.fields['reviewed_by'].widget.attrs.update({'class': 'form-select'})  # Add Bootstrap styling

        if user:
            if user.is_staff or user.is_superuser:  
                # If the logged-in user is admin or staff, restrict reviewed_by field
                self.fields['reviewed_by'].queryset = User.objects.filter(employee_id=user.employee_id)  # FIXED HERE
                self.fields['reviewed_by'].initial = user
                self.fields['reviewed_by'].widget.attrs['readonly'] = True  # Make it readonly
                self.fields['reviewed_by'].widget.attrs['class'] += ' form-control-plaintext'  # Display as plain text
            else:
                # If not admin/staff, remove 'reviewed_by' field (prevents them from setting it)
                self.fields.pop('reviewed_by', None) 


from django import forms
from .models import Leave

# class LeaveApplicationForm(forms.ModelForm):
#     class Meta:
#         model = Leave
#         fields = ['leave_type', 'reason', 'start_date', 'end_date']

class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['leave_type', 'reason', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'required': True}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'required': True}),
        }
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date must be after start date.")

        return cleaned_data


class LeaveApprovalForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['status']

    def clean_status(self):
        status = self.cleaned_data.get('status')
        if status not in ['approved', 'rejected']:
            raise forms.ValidationError("Invalid status selection.")
        return status
