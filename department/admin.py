from django.contrib import admin
from .models import Department,Roles,Employe_User
# Register your models here.

class adminDepartmentmodel(admin.ModelAdmin):
    list_display = ['department_name','department_description']
admin.site.register(Department,adminDepartmentmodel)


class adminRolesmodel(admin.ModelAdmin):
    list_display = ['role_name','role_description']
admin.site.register(Roles,adminRolesmodel)


class adminEmployeemodel(admin.ModelAdmin):
    list_display = ['employee_id','first_name','username']
admin.site.register(Employe_User,adminEmployeemodel)

 

from django.contrib import admin
from .models import Task, TaskAssignment

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_title', 'task_priority', 'start_date', 'end_date', 'task_type', 'created_at', 'updated_at')
    search_fields = ('task_title', 'task_priority', 'task_type')
    list_filter = ('task_priority', 'task_type', 'start_date', 'end_date')

@admin.register(TaskAssignment)
class TaskAssignmentAdmin(admin.ModelAdmin):
    list_display = ('task', 'employee', 'assigned_by', 'assigned_date', 'status', 'completed_at')
    search_fields = ('task__task_title', 'employee__first_name', 'assigned_by__first_name', 'status')
    list_filter = ('status', 'assigned_date', 'completed_at')
    
####
from django.contrib import admin
from .models import PerformanceReview

@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'review_title', 'employee', 'reviewed_by', 'review_period', 'rating', 'review_date')
    search_fields = ('review_title', 'employee__first_name', 'reviewed_by__first_name')
    list_filter = ('review_period', 'rating')



from django.contrib import admin
from .models import Leave, LeaveQuota

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'total_days', 'status', 'approved_by')
    list_filter = ('status', 'leave_type', 'start_date', 'end_date')
    search_fields = ('employee__username', 'approved_by__username', 'leave_type')
    ordering = ('-start_date',)
    list_editable = ('status',)
    readonly_fields = ('total_days',)

@admin.register(LeaveQuota)
class LeaveQuotaAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'total_quota', 'used_quota', 'remain_quota')
    search_fields = ('employee__username',)
    list_filter = ('leave_type',)

    def remain_quota(self, obj):
        return obj.total_quota - obj.used_quota
    remain_quota.short_description = 'Remaining Quota'



