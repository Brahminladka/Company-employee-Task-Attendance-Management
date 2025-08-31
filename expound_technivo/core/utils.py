from django.db import connection

def update_employee_managers(employee_id, manager_ids):
    """
    Update the employee_manager_mapping table for the given employee.
    Clears existing mappings and inserts new ones.
    """
    with connection.cursor() as cursor:
        # Remove existing mappings
        cursor.execute(
            "DELETE FROM employee_manager_mapping WHERE employee_id = %s", [employee_id]
        )

        # Insert new mappings
        for mgr_id in manager_ids:
            cursor.execute(
                "INSERT INTO employee_manager_mapping (employee_id, manager_id) VALUES (%s, %s)",
                [employee_id, mgr_id]
            )
