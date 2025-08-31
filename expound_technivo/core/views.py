# core/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Employee, ProjectMaster, Attendance, LoginCredential
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
from django.contrib.auth.hashers import make_password
import random, string
from django.utils import timezone
from django.conf import settings
from functools import wraps
from django.db.models import F , Q
from django.db import transaction, connection
from django.core.serializers.json import DjangoJSONEncoder
import json
from .utils import update_employee_managers 

# Custom decorator to check login via session
def login_required_custom(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if "username" not in request.session:
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper


# Login view to handle user authentication
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = LoginCredential.objects.get(username=username)
        except LoginCredential.DoesNotExist:
            messages.error(request, "Invalid username or password")
            return redirect("login")

        # check if related employee exists and is active
        try:
            employee = Employee.objects.get(employee_code=user.employee_code)
            if not employee.status:  # if inactive
                messages.error(request, "Your account is inactive. Please contact HR.")
                return redirect("login")
        except Employee.DoesNotExist:
            messages.error(request, "Employee record not found. Please contact HR.")
            return redirect("login")

        # check password
        if check_password(password, user.password_hash) or password == user.password:
            # Save session
            request.session["username"] = user.username
            request.session["role"] = user.department  # HR, Manager, Employee
            request.session["employee_code"] = employee.employee_code
            request.session["employee_name"] = employee.name

            # ✅ always redirect to single dashboard
            return redirect("dashboard")

        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")

    return render(request, "login.html")

@login_required_custom
def dashboard(request):
    username = request.session.get("username")
    role = request.session.get("role")  # HR, Manager, Employee

    employee = None
    if username:
        try:
            credential = LoginCredential.objects.get(username=username)
            employee = Employee.objects.get(employee_code=credential.employee_code)
        except (LoginCredential.DoesNotExist, Employee.DoesNotExist):
            employee = None
    

    statuses = ["Not Started", "Work In Progress"]

    if role == "HR":
        # HR sees all employees
        total_employees = Employee.objects.filter(status=1).count()
        pending_tasks = Attendance.objects.filter(
            employee_code=employee.employee_code,
            status__in=statuses
        ).count()

    elif role == "MANAGER":
        # Get employees under this manager using raw SQL
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT e.employee_code
                FROM employee e
                INNER JOIN employee_manager_mapping emm ON e.id = emm.employee_id
                INNER JOIN employee m ON emm.manager_id = m.id
                WHERE m.employee_code = %s
            """, [employee.employee_code])
            employee_codes = [row[0] for row in cursor.fetchall()]

        total_employees = len(employee_codes)

        # Fetch pending tasks for employees under this manager
        pending_tasks = Attendance.objects.filter(
            employee_code__in=employee_codes,
            status__in=statuses
        ).count()

    else :
        total_employees = 1
        pending_tasks = Attendance.objects.filter(
            employee_code=employee.employee_code,
            status__in=statuses
        ).count()


    # Send to template
    return render(request, "dashboard.html", {
        "employee": employee,
        "role": role,
        "total_employees": total_employees,
        "pending_tasks": pending_tasks,
    })


# Employees
@login_required_custom
def employee_list(request):
    role = request.session.get("role")
    employee_code = request.session.get("employee_code")

    employees = Employee.objects.none()  # default empty

    if role == "HR":
        # HR sees all
        employees = Employee.objects.all()

    elif role == "MANAGER":
        # Manager sees employees under him (via raw SQL mapping)
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT e.id
                FROM employee e
                INNER JOIN employee_manager_mapping emm ON e.id = emm.employee_id
                INNER JOIN employee m ON emm.manager_id = m.id
                WHERE m.employee_code = %s
            """, [employee_code])
            employee_ids = [row[0] for row in cursor.fetchall()]

        employees = Employee.objects.filter(id__in=employee_ids)

    elif role == "EMPLOYEE":
        # Employee sees only self
        employees = Employee.objects.filter(employee_code=employee_code)

    return render(request, "list/employee_list.html", {"employees": employees})
# Add Employee
def generate_password(length=8):
    """Generate random 8-character alphanumeric password"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def employee_add(request):
    if request.method == "POST":
        employee = Employee.objects.create(
            employee_code=request.POST["employee_code"],
            name=request.POST["name"],
            department=request.POST["department"],
            doj=request.POST["doj"],
            exit_date=request.POST.get("exit_date") or None,
            status=request.POST.get("status") == "Active",
        )

        # Get manager names from hidden input (comma-separated)
        # Get manager codes from hidden input (comma-separated)
        manager_codes = request.POST.get("manager_codes", "")
        if manager_codes:
            # Convert codes to manager IDs
            manager_ids = list(Employee.objects.filter(employee_code__in=manager_codes.split(",")).values_list("id", flat=True))
            update_employee_managers(employee.id, manager_ids)

        
        username = f"EMP00{employee.employee_code}"
        raw_password = generate_password()
        password_hash = make_password(raw_password)

        LoginCredential.objects.create(
            employee_code=employee.employee_code,
            username=username,
            name=employee.name,
            department=employee.department,
            password=raw_password,
            password_hash=password_hash,
        )

        messages.success(request, f"Employee added successfully. Username: {username}, Password: {raw_password}")
        return redirect("employee_list")

    # Send full manager objects but use only names in template
    managers = Employee.objects.filter(department="MANAGER")
    departments = Employee.objects.values_list("department", flat=True).distinct()
    current_manager_codes = []
    if 'employee' in locals() and employee:
        # List of dictionaries {code, name}
        current_manager_codes = list(employee.managers.values('employee_code', 'name'))

    return render(request, "form/employee_form.html", {
        "employee": employee if 'employee' in locals() else None,
        "departments": departments,
        "managers": managers,
        "current_manager_codes_json": json.dumps(current_manager_codes, cls=DjangoJSONEncoder),
    })


# Edit Employee
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == "POST":
        employee.employee_code = request.POST["employee_code"]
        employee.name = request.POST["name"]
        employee.department = request.POST["department"]
        employee.doj = request.POST["doj"]
        employee.exit_date = request.POST.get("exit_date") or None
        employee.status = request.POST.get("status") == "Active"
        employee.save()

        # Get manager codes from hidden input (comma-separated)
        manager_codes = request.POST.get("manager_codes", "")
        if manager_codes:
            manager_ids = list(Employee.objects.filter(
                employee_code__in=manager_codes.split(",")
            ).values_list("id", flat=True))
            update_employee_managers(employee.id, manager_ids)

        messages.success(request, "Employee updated successfully")
        return redirect("employee_list")

    departments = Employee.objects.values_list("department", flat=True).distinct()
    managers = Employee.objects.filter(department="MANAGER")

    # Preload managers manually
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT manager_id FROM employee_manager_mapping WHERE employee_id=%s",
            [employee.id]
        )
        current_manager_ids = [row[0] for row in cursor.fetchall()]
    current_managers = Employee.objects.filter(id__in=current_manager_ids)

    return render(request, "form/employee_form.html", {
        "employee": employee,
        "departments": departments,
        "managers": managers,
        "current_managers": current_managers,  # <--- pass this to template
    })


# Projects
def project_list(request):
    projects = ProjectMaster.objects.all()
    return render(request, "list/project_list.html", {"projects": projects})

@login_required_custom
def project_add(request):
    if request.method == "POST":
        ProjectMaster.objects.create(
            project_code=request.POST["project_code"],
            cost_category_project_type=request.POST["cost_category_project_type"],
            cost_centre_client_name=request.POST["cost_centre_client_name"],
            issue_id=request.POST["issue_id"],
            issue_date=request.POST["issue_date"],
            issue_by=request.POST["issue_by"],
            status="1",
        )
        messages.success(request, "Project added successfully")
        return redirect("project_list")

    # Fetch only managers from LoginCredential
    managers = LoginCredential.objects.filter(department="MANAGER")
    
    cost_categories = ProjectMaster.objects.values_list("cost_category_project_type", flat=True).distinct()
    cost_centres = ProjectMaster.objects.values_list("cost_centre_client_name", flat=True).distinct()
    issues = ProjectMaster.objects.values_list("issue_id", flat=True).distinct()

    return render(request, "form/project_form.html", {"managers": managers, "cost_categories": cost_categories, "cost_centres": cost_centres, "issues": issues,})

def project_edit(request, pk):
    project = get_object_or_404(ProjectMaster, pk=pk)
    if request.method == "POST":
        project.cost_category = request.POST["cost_category"]
        project.cost_centre = request.POST["cost_centre"]
        project.manager_name = request.POST["manager_name"]
        project.remark = request.POST["remark"]
        project.save()
        messages.success(request, "Project updated successfully")
        return redirect("project_list")
    return render(request, "project_form.html", {"project": project})

# Attendance
def attendance_list(request):
    attendance = Attendance.objects.all().order_by('-work_date')
    # Check if a date is selected in GET parameters
    selected_date = request.GET.get('work_date')
    if selected_date:
        attendance = attendance.filter(work_date=selected_date)

    return render(request, "list/attendance_list.html", {
        "attendance": attendance,
        "selected_date": selected_date,  # send it back to template
    })


@csrf_exempt
def attendance_update(request, pk):
    att = get_object_or_404(Attendance, pk=pk)

    if request.method == "POST":
        field = request.POST.get("field")   # which field we are updating
        value = request.POST.get("value")

        if field == "remark":
            att.remark = value

        elif field == "hrs":
            try:
                att.hrs = float(value) if value else None
            except ValueError:
                return JsonResponse({"success": False, "error": "Invalid hrs"}, status=400)

        elif field == "exit_date":
            att.exit_date = parse_date(value) if value else None

        elif field == "status":
            att.status = value

        else:
            return JsonResponse({"success": False, "error": "Invalid field"}, status=400)

        att.save()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False}, status=400)
 
# Delete Attendance 
def attendance_delete(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    if request.method == "POST":
        attendance.delete()
        messages.add_message(request, settings.ATTENDANCE_DELETED, "Attendance record deleted successfully")
        return redirect("attendance_list")
    # Optional: you could render a confirmation page here
    return redirect("attendance_list")

# Login Credentials
def login_list(request):
    logins = LoginCredential.objects.all()
    return render(request, "list/login_list.html", {"logins": logins})


# Manager Ticket Raise
@login_required_custom
def ticket_raise(request):
    if request.method == "POST":
        employee_code = request.POST.get("employee_code")
        project_code = request.POST.get("project_code")
        issue_id = request.POST.get("issue_id")
        completed_date = request.POST.get("completed_date")
        remark = request.POST.get("remark")

        # Get employee object
        try:
            emp = Employee.objects.get(employee_code=employee_code)
        except Employee.DoesNotExist:
            messages.add_message(request, settings.TICKET_REJECTED, "Employee does not exist.")
            return redirect("ticket_raise")

        if emp.status != 1:
            messages.add_message(request, settings.TICKET_REJECTED, "This employee is not active.")
            return redirect("ticket_raise")

        # Get project details
        try:
            project = ProjectMaster.objects.get(project_code=project_code)
        except ProjectMaster.DoesNotExist:
            messages.add_message(request, settings.TICKET_REJECTED, "Invalid project code.")
            return redirect("ticket_raise")

        # Manager details (fetch full name instead of username)
        # Get logged-in employee from session
        username = request.session.get("username")  # session key set in login_view
        if username:
            try:
                # Get the corresponding employee object
                logged_in_employee = Employee.objects.get(employee_code=LoginCredential.objects.get(username=username).employee_code)
                manager_name = logged_in_employee.name
            except (Employee.DoesNotExist, LoginCredential.DoesNotExist):
                manager_name = username
        else:
            manager_name = "Unknown"

        # Save into Attendance table
        Attendance.objects.create(
            employee_code=emp.employee_code,
            name=emp.name,
            doj=emp.doj,
            department=emp.department,
            work_date=timezone.now().date(),
            work_day=timezone.now().weekday() + 1,
            project_code=project.project_code,
            cost_category=project.cost_category_project_type,
            cost_centre=project.cost_centre_client_name,
            issue_id=issue_id,
            manager_name=manager_name,
            remark=remark,
            status="Not Started",
            completed_date=completed_date
        )

        # ✅ Custom success message
        messages.add_message(request, settings.TICKET_RAISED, "Ticket raised successfully!")
        return redirect("ticket_raise")

    employees = Employee.objects.all()
    projects = ProjectMaster.objects.all()
    return render(request, "form/ticket_raise.html", {"employees": employees, "projects": projects})

# -------- AJAX Views --------

def get_employee_details(request):
    """Auto populate employee details"""
    emp_code = request.GET.get("employee_code")
    try:
        emp = Employee.objects.get(employee_code=emp_code)
        return JsonResponse({
            "name": emp.name,
            "department": emp.department,
            "doj": emp.doj.strftime("%Y-%m-%d"),
        })
    except Employee.DoesNotExist:
        return JsonResponse({}, status=404)


def get_project_details(request):
    """Auto populate project details"""
    proj_code = request.GET.get("project_code")
    try:
        proj = ProjectMaster.objects.get(project_code=proj_code)
        return JsonResponse({
            "cost_category": proj.cost_category_project_type,
            "cost_centre": proj.cost_centre_client_name,
            "issue_id": proj.issue_id,
        })
    except ProjectMaster.DoesNotExist:
        return JsonResponse({}, status=404)
    

@login_required_custom
def get_project_codes(request):
    """Return matching project codes based on selected category, centre, issue"""
    cost_category = request.GET.get("cost_category")
    cost_centre = request.GET.get("cost_centre")
    issue_id = request.GET.get("issue_id")

    qs = ProjectMaster.objects.all()

    if cost_category:
        qs = qs.filter(cost_category_project_type=cost_category)
    if cost_centre:
        qs = qs.filter(cost_centre_client_name=cost_centre)
    if issue_id:
        qs = qs.filter(issue_id=issue_id)
    
    projects = [{"project_code": p.project_code, "client_name": p.cost_centre_client_name} for p in qs.distinct()]
    cost_categories = list(qs.values_list("cost_category_project_type", flat=True).distinct())
    cost_centres = list(qs.values_list("cost_centre_client_name", flat=True).distinct())
    issue_ids = list(qs.values_list("issue_id", flat=True).distinct())

    return JsonResponse({"projects": projects,"cost_categories": cost_categories,"cost_centres": cost_centres,"issue_ids": issue_ids,})  
    
# My Tickets View
@login_required_custom
def my_tickets_view(request):
    username = request.session.get("username")
    role = request.session.get("role", "").lower()  # HR / Manager / Employee

    tickets = Attendance.objects.none()  # Default empty

    if not username:
        # Not logged in
        return render(request, "list/my_tickets.html", {"tickets": tickets})

    try:
        login_user = LoginCredential.objects.get(username=username)
    except LoginCredential.DoesNotExist:
        return render(request, "list/my_tickets.html", {"tickets": tickets})

    if role == "manager":
        # Manager sees tickets assigned to them, along with who it's shared with
        manager_name = login_user.name
        tickets = Attendance.objects.filter(manager_name=manager_name) \
            .prefetch_related("shared_with") \
            .order_by(F("completed_date").asc(nulls_last=True))

    else:
        # Employee sees tickets they raised OR tickets shared with them
        tickets = Attendance.objects.filter(
            Q(employee_code=login_user.employee_code) |
            Q(shared_with__employee_code=login_user.employee_code)
        ).distinct().order_by(F("completed_date").asc(nulls_last=True)) \
         .prefetch_related("shared_with")
        
    employees = LoginCredential.objects.all()
    return render(request, "list/my_tickets.html", {"tickets": tickets, "employees": employees})

# Delete Ticket
@login_required_custom
def ticket_delete(request, pk):
    ticket = get_object_or_404(Attendance, pk=pk)  # Or Ticket model
    if request.method == "POST":
        ticket.delete()
        messages.success(request, "Ticket deleted successfully")
        return redirect("my_tickets")  # Your ticket list URL
    return redirect("my_tickets")

# Update Ticket (AJAX)
@csrf_exempt
@login_required_custom
def ticket_update(request, pk):
    ticket = get_object_or_404(Attendance, pk=pk)  # or Ticket model if separate

    role = request.session.get("role")  # HR / Manager / Employee

    if request.method == "POST":
        field = request.POST.get("field")
        value = request.POST.get("value")

        # Check if completed_date expired
        if ticket.completed_date and ticket.completed_date < timezone.now().date():
            if role.lower() != "manager":  
                return JsonResponse({
                    "success": False,
                    "error": "You cannot update this ticket as the completion date has passed."
                }, status=403)

        # Allow update if rules are passed
        if field == "remark":
            ticket.remark = value
        elif field == "status":
            ticket.status = value
        elif field == "completed_date":
            ticket.completed_date = value  # should be YYYY-MM-DD
        # Add more fields if needed

        ticket.save()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

# Share Ticket (Alternative)
@csrf_exempt
@login_required_custom
def ticket_share_view(request):
    if request.method == "POST":
        ticket_id = request.POST.get("ticket_id")
        employee_codes = request.POST.getlist("employee_codes[]")

        try:
            with transaction.atomic():  # ✅ Add transaction protection
                ticket = Attendance.objects.get(pk=ticket_id)
                employees = LoginCredential.objects.filter(employee_code__in=employee_codes)
                ticket.shared_with.set(employees)
                # No need for ticket.save() - set() handles it
            return JsonResponse({"success": True, "shared_count": employees.count()})
        except Attendance.DoesNotExist:
            return JsonResponse({"success": False, "error": "Ticket not found"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request method"})

