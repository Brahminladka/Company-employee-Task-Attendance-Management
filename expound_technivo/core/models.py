from django.db import models
from django.contrib.auth.hashers import make_password
from django.db import models
from django.db import connection

class Employee(models.Model):
    employee_code = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    doj = models.DateField()
    status = models.BooleanField(default=True)
    exit_date = models.DateField(null=True, blank=True)  # NULL allowed
    ROLE_CHOICES = (
        ("HR", "HR"),
        ("MANAGER", "MANAGER"),
        ("EMPLOYEE", "EMPLOYEE"),
    )
    role = models.CharField(max_length=20,choices=ROLE_CHOICES,default="EMPLOYEE")
    managers = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="team_members",
        blank=True,
        db_table="employee_manager_mapping",  # uses your existing table
        
    )

    @property
    def manager_names_display(self):
        """Fetch distinct manager names from the mapping table using SQL."""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT e2.name
                FROM employee_manager_mapping em
                JOIN employee e1 ON e1.id = em.employee_id
                JOIN employee e2 ON e2.id = em.manager_id
                WHERE e1.id = %s
            """, [self.id])
            rows = cursor.fetchall()
        if rows:
            # Sort alphabetically if you want consistent order
            manager_names = sorted(set(r[0] for r in rows))
            return ", ".join(manager_names)
        return "No managers"

    class Meta:
        db_table = "employee"


    def __str__(self):
        return f"{self.employee_code} - {self.name}"
    
    # helper to update manager_names automatically
    def update_manager_names(self):
        self.manager_names = ", ".join([m.name for m in self.managers.all()])
        self.save()

    @property
    def manager_names_str(self):
        if self.managers.exists():
            return ", ".join([m.name for m in self.managers.all()])
        return "No managers"


class Attendance(models.Model):
    employee_code = models.IntegerField()
    name = models.CharField(max_length=100)
    doj = models.DateField()
    department = models.CharField(max_length=50)
    work_date = models.DateField()
    work_day = models.IntegerField()
    project_code = models.CharField(max_length=50)
    cost_category = models.CharField(max_length=100)
    cost_centre = models.CharField(max_length=100)
    issue_id = models.CharField(max_length=50)
    manager_name = models.CharField(max_length=100)
    remark = models.TextField()
    hrs = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    exit_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Not Started', 'Not Started'),
            ('Work In Progress', 'Work In Progress'),
            ('Completed', 'Completed')
        ],
        default="Not Started"
    )
    completed_date = models.DateField(null=True, blank=True)
    shared_with = models.ManyToManyField(
        'LoginCredential', 
        blank=True,
        related_name='shared_tickets',
        help_text="Employees with whom this ticket is shared",
        db_table='attendance_shared_with'
    )

    class Meta:
        db_table = "attendance"


class LoginCredential(models.Model):
    employee_code = models.IntegerField(unique=True)
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    password_hash = models.CharField(max_length=255)
    password = models.CharField(max_length=8)

    class Meta:
        db_table = "login_credential"


class ProjectMaster(models.Model):
    project_code = models.CharField(max_length=50)
    cost_category_project_type = models.CharField(max_length=100)
    cost_centre_client_name = models.CharField(max_length=100)
    issue_id = models.CharField(max_length=50)
    issue_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=1,
        choices=[('1','Not Started'),
                 ('2','Work In Progress'),
                 ('3','Completed')]
    )
    issue_by = models.CharField(max_length=100)

    class Meta:
        db_table = "project_master"
