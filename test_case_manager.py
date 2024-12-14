import sqlite3
import pytest
from datetime import datetime

def connect_db():
    return sqlite3.connect('task_manager.db')

@pytest.fixture(scope="module")
def setup_db():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        start_date DATE NOT NULL,
        due_date DATE NOT NULL,
        person_responsible TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Not Started'
    );
    ''')
    conn.commit()
    yield conn
    cursor.execute("DROP TABLE IF EXISTS tasks")
    conn.commit()
    conn.close()

def test_create_task(setup_db):
    conn = setup_db
    cursor = conn.cursor()

    task_data = ('Complete Project', '2024-12-15', '2024-12-20', 'Shamik Patel')

    cursor.execute('''
    INSERT INTO tasks (task, start_date, due_date, person_responsible, status)
    VALUES (?, ?, ?, ?, ?)
    ''', task_data + ('Not Started',))
    conn.commit()

    cursor.execute('SELECT * FROM tasks WHERE task=?', ('Complete Project',))
    task = cursor.fetchone()
    
    assert task is not None
    assert task[1] == 'Complete Project'
    assert task[2] == '2024-12-15'
    assert task[3] == '2024-12-20'
    assert task[4] == 'Shamik Patel'
    assert task[5] == 'Not Started'

def test_update_task(setup_db):
    conn = setup_db
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO tasks (task, start_date, due_date, person_responsible, status)
    VALUES (?, ?, ?, ?, ?)
    ''', ('Test Task', '2024-12-10', '2024-12-15', 'Shamik', 'Not Started'))
    conn.commit()

    cursor.execute('''
    UPDATE tasks SET status=? WHERE task=?
    ''', ('In Progress', 'Test Task'))
    conn.commit()

    cursor.execute('SELECT * FROM tasks WHERE task=?', ('Test Task',))
    task = cursor.fetchone()

    assert task[5] == 'In Progress'

def test_delete_task(setup_db):
    conn = setup_db
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO tasks (task, start_date, due_date, person_responsible, status)
    VALUES (?, ?, ?, ?, ?)
    ''', ('Task to Delete', '2024-12-01', '2024-12-05', 'Shamik', 'Not Started'))
    conn.commit()

    cursor.execute('''
    DELETE FROM tasks WHERE task=?
    ''', ('Task to Delete',))
    conn.commit()

    cursor.execute('SELECT * FROM tasks WHERE task=?', ('Task to Delete',))
    task = cursor.fetchone()

    assert task is None

def test_get_tasks_by_status(setup_db):
    conn = setup_db
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO tasks (task, start_date, due_date, person_responsible, status)
    VALUES (?, ?, ?, ?, ?)
    ''', ('Task 1', '2024-12-10', '2024-12-15', 'Shamik Patel', 'Not Started'))
    cursor.execute('''
    INSERT INTO tasks (task, start_date, due_date, person_responsible, status)
    VALUES (?, ?, ?, ?, ?)
    ''', ('Task 2', '2024-12-11', '2024-12-16', 'Shamik', 'In Progress'))
    conn.commit()

    cursor.execute('SELECT * FROM tasks WHERE status=?', ('Not Started',))
    tasks = cursor.fetchall()

    assert len(tasks) == 1
    assert tasks[0][1] == 'Task 1'
    assert tasks[0][5] == 'Not Started'

def test_get_tasks_by_person(setup_db):
    conn = setup_db
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO tasks (task, start_date, due_date, person_responsible, status)
    VALUES (?, ?, ?, ?, ?)
    ''', ('Task A', '2024-12-01', '2024-12-05', 'Shamik Patel', 'Not Started'))
    cursor.execute('''
    INSERT INTO tasks (task, start_date, due_date, person_responsible, status)
    VALUES (?, ?, ?, ?, ?)
    ''', ('Task B', '2024-12-02', '2024-12-06', 'Patel', 'Completed'))
    cursor.execute('''
    INSERT INTO tasks (task, start_date, due_date, person_responsible, status)
    VALUES (?, ?, ?, ?, ?)
    ''', ('Task C', '2024-12-03', '2024-12-07', 'Shamik', 'In Progress'))
    conn.commit()

    cursor.execute('SELECT * FROM tasks WHERE person_responsible=?', ('Shamik Patel',))
    tasks = cursor.fetchall()

    assert len(tasks) == 2
    assert tasks[0][1] == 'Task A'
    assert tasks[1][1] == 'Task B'

if __name__ == '__main__':
    pytest.main()
