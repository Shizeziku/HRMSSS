from django.db import models
from django.utils import timezone


# Create your models here.

class Department(models.Model):
    department_name = models.CharField(max_length=100, blank=True,null=True)
    department_description = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.department_name



class Roles(models.Model):
    role_name = models.CharField(max_length=100, blank=True,null=True)
    role_description = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.role_name
    

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class Employe_User(AbstractUser):
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=100, unique=True)
    dept = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="employees")
    role = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True, related_name="users")
    reporting_manager = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True,related_name="team_members")
    date_of_joining = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    username = models.CharField(max_length=150, unique=True, blank=False)
    password = models.CharField(max_length=128)  # Django stores hashed passwords

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_set",
        blank=True
    )
  
    def save(self, *args, **kwargs):
        if not self.reporting_manager:
            hr_admin = Employe_User.objects.filter(role__role_name="HR").first()
            self.reporting_manager = hr_admin if hr_admin else None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role.role_name if self.role else 'No Role'}"