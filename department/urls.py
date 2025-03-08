from django.urls import path
from .import views

urlpatterns = [
     path('add',views.add,name="add"),
     path('',views.home,name="home"),
     path('delete/<int:id>/', views.delete_product, name='deleteprod'), 
     path('updateprod/<int:id>/',views.updateprod,name='updateprod'),    
     path('register/',views.register,name="register"),
     path('login/',views.user_login,name="login"),
     path('logout1/',views.logout_details,name="logout1"),
     path('roles/',views.roles,name="roles"),
     path('deleterole/<int:id>/', views.deleterole, name='deleterole'), 
     path('updaterole/<int:id>/',views.updaterole,name='updaterole'),
     path('employees/', views.create_employee, name='employee_list'),
     path('Forgot_Password/', views.Forgot_pass, name='Forgotpass'),  # Add this new view
     path('success/', views.success_page, name='success_page'),
     path('reset_password/<uidb64>/<token>/', views.reset_password, name='resetpassword'),
     path('password_reset_done/', views.password_reset_done, name='passwordresetdone'),
     
     path('user_dashboard',views.user_dashboard,name='user_dashboard'),
     #######################
     path('task_list/', views.task_list, name='task_list'),
     path('task/create/', views.task_create, name='task_create'),
     path('task/update/<int:task_id>/', views.task_update, name='task_update'),
     path('task/delete/<int:task_id>/', views.task_delete, name='task_delete'),
     path('task/assign/', views.assign_task, name='assign_task'),
    # path('task/update-status/<int:assignment_id>/', views.update_task_status, name='update_task_status'),

    path('reviews/', views.performance_reviews, name='review_list'),
    path('reviews/add/', views.add_review, name='add_review'),
    path('reviews/edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('reviews/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    
    ###################################################################################
    
    path('apply/', views.apply_leave, name='apply_leave'),
    path('status/', views.leave_status, name='leave_status'),
    path('approve/<int:leave_id>/', views.approve_leave, name='approve_leave'),
    ###################################################################################
    #  path('view-leaves/', view_leave_applications, name='view_leave_applications'),
    # path('approve-leave/<int:leave_id>/', approve_leave, name='approve_leave'),
    # path('reject-leave/<int:leave_id>/', reject_leave, name='reject_leave'),
    path('employee-leave-data/', views.employee_leave_data, name='employee_leave_data'),
    # path('modify-leave/<int:leave_id>/', modify_leave_records, name='modify_leave_records'),
    # path('view-employee-leaves/<int:employee_id>/', view_employee_leaves, name='view_employee_leaves'),
]





     

     

    


