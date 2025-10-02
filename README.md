# 📌 Company Employee, Task & Attendance Management

## 🔹 Overview
This is a **Django-based web application** for managing **employees, tasks, and attendance** in a company.  
It uses **MySQL** as the backend database and provides a simple, user-friendly interface to track employees, assign tasks, and manage attendance.

---

## 🔹 Features
- Employee CRUD (Create, Read, Update, Delete)
- Task assignment and management
- Attendance tracking (add, edit, delete)
- Request approval/rejection workflow
- Holiday management (upload and count)
- Dashboard for overview of company operations

---

## 🔹 Installation & Setup

### Step 1: Prerequisites
1. **Python 3.8+** → [Download Python](https://www.python.org/downloads/)
2. **MySQL Server** → [Download MySQL](https://dev.mysql.com/downloads/)
3. Install required Python packages:

```bash
pip install django mysqlclient
```

- **django** → Web framework
- **mysqlclient** → Connect Django with MySQL database

---

### Step 2: Clone Project & Configure Database
1. Download project files: [Google Drive Link](https://drive.google.com/file/d/1x-a3Aqt8qajUB5JZ7-bGqDaNNaAiJ4vD/view?usp=sharing)  
2. Update `settings.py` with your MySQL credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

---

### Step 3: Migrate Database
```bash
python manage.py makemigrations
python manage.py migrate
```

---

### Step 4: Create Superuser (Admin)
```bash
python manage.py createsuperuser
```
Follow the prompts to create admin credentials.

---

### Step 5: Run Server
```bash
python manage.py runserver
```
Open your browser at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)  

---

## 🔹 URL Patterns (Highlights)
- `/login/` → Login page
- `/dashboard/` → Dashboard overview
- `/employees/` → Employee list
- `/employees/add/` → Add employee
- `/employees/edit/<int:pk>/` → Edit employee
- `/tasks/` → Task list
- `/tasks/<int:pk>/edit/` → Edit task
- `/attendance/` → Attendance list
- `/attendance/new/` → Add attendance
- `/attendance/edit/<int:pk>/` → Edit attendance
- `/requests/` → Request list
- `/request/<int:pk>/<str:action>/` → Approve/Reject request

---

## 🔹 Skills & Tools Used
- **Languages:** Python, HTML, CSS, JavaScript
- **Framework:** Django
- **Database:** MySQL
- **Libraries:** Django ORM, Bootstrap
- **Tools:** VS Code, MySQL Workbench

---

## 🔹 Outcome
- Full-stack CRUD operations for employees, tasks, and attendance  
- Role-based request and task management  
- Hands-on experience integrating Django with MySQL  
- Dashboard providing a clear overview of company operations

---

## 🔹 Demo / Files
📂 Project Files: [Google Drive Link](https://drive.google.com/file/d/1x-a3Aqt8qajUB5JZ7-bGqDaNNaAiJ4vD/view?usp=sharing)
