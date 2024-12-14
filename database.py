import sqlite3

def initialize_database():
    connection = sqlite3.connect("task_manager.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            start_date DATE NOT NULL,
            due_date DATE NOT NULL,
            responsible_person TEXT NOT NULL,
            status TEXT DEFAULT 'Not Started'
        )
    """)
    connection.commit()
    connection.close()

# Add a Task
def create_task(task_name, start_date, due_date, responsible_person, status="Not Started"):
    connection = sqlite3.connect("task_manager.db")
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO tasks (task_name, start_date, due_date, responsible_person, status)
        VALUES (?, ?, ?, ?, ?)
    """, (task_name, start_date, due_date, responsible_person, status))
    connection.commit()
    connection.close()

# Retrieve All Tasks
def retrieve_tasks():
    connection = sqlite3.connect("task_manager.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    connection.close()
    return tasks

# Update a Task
def update_task(task_id, task_name, start_date, due_date, responsible_person, status):
    connection = sqlite3.connect("task_manager.db")
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE tasks
        SET task_name = ?, start_date = ?, due_date = ?, responsible_person = ?, status = ?
        WHERE id = ?
    """, (task_name, start_date, due_date, responsible_person, status, task_id))
    connection.commit()
    connection.close()

# Delete a Task
def delete_task(task_id):
    connection = sqlite3.connect("task_manager.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    connection.commit()
    connection.close()

# Filter Tasks by Status
def filter_tasks_by_status(status):
    connection = sqlite3.connect("task_manager.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks WHERE status = ?", (status,))
    tasks = cursor.fetchall()
    connection.close()
    return tasks

# Filter Tasks by Person
def filter_tasks_by_responsible_person(person):
    connection = sqlite3.connect("task_manager.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks WHERE responsible_person LIKE ?", ('%' + person + '%',))
    tasks = cursor.fetchall()
    connection.close()
    return tasks
