from django.urls import path
from . import views
from .views import login_view, dashboard

urlpatterns = [
    # Login
    path("login/", views.login_view, name="login"),

    # Single Dashboard for all
    path("dashboard/", views.dashboard, name="dashboard"),

    # Employee CRUD
    path("hr/employees/", views.employee_list, name="employee_list"),
    path("hr/employees/add/", views.employee_add, name="employee_add"),
    path("hr/employees/edit/<int:pk>/", views.employee_edit, name="employee_edit"),

    # Project CRUD
    path("hr/projects/", views.project_list, name="project_list"),
    path("hr/projects/add/", views.project_add, name="project_add"),
    path("hr/projects/edit/<int:pk>/", views.project_edit, name="project_edit"),

    # Attendance
    path("hr/attendance/", views.attendance_list, name="attendance_list"),
    path("attendance/update/<int:pk>/", views.attendance_update, name="attendance_update"),
    path("hr/attendance/delete/<int:pk>/", views.attendance_delete, name="attendance_delete"),

    # Login Credentials
    path("hr/logins/", views.login_list, name="login_list"),

    # Manager Ticket Raise
    path("ticket-raise/", views.ticket_raise, name="ticket_raise"),
    path("tickets/my/", views.my_tickets_view, name="my_tickets"),
    path("tickets/update/<int:pk>/", views.ticket_update, name="ticket_update"),
    path("tickets/delete/<int:pk>/", views.ticket_delete, name="ticket_delete"),
    path("get-employee-details/", views.get_employee_details, name="get_employee_details"),
    path("get-project-details/", views.get_project_details, name="get_project_details"),
    path("tickets/share/", views.ticket_share_view, name="ticket_share"),
    path('get_project_codes/', views.get_project_codes, name='get_project_codes')


]
