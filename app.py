import sqlite3
import streamlit as st
from datetime import date
from database import (
    initialize_database,
    create_task,
    retrieve_tasks,
    update_task,
    delete_task,
    filter_tasks_by_status,
    filter_tasks_by_responsible_person,
)


DB_PATH = 'database/task_manager.db'

def connect_db():
    return sqlite3.connect(DB_PATH)


initialize_database()

st.title("Task Manager Application")
menu_option = st.sidebar.selectbox("Menu", ["Create Task", "View Tasks", "Reports"])

if menu_option == "Create Task":
    st.header("Create a New Task")
    task_name = st.text_input("Task Name")
    start_date = st.date_input("Start Date", min_value=date.today())
    due_date = st.date_input("Due Date", min_value=start_date)
    responsible_person = st.text_input("Responsible Person(s) (comma-separated)")
    status_options = ["Not Started", "In-Progress", "Completed"]
    status = st.selectbox("Status", status_options, index=0)

    if st.button("Add Task"):
        if task_name and responsible_person:
            create_task(task_name, start_date, due_date, responsible_person, status)
            st.success("Task added successfully!")
        else:
            st.error("Please fill all required fields.")

elif menu_option == "View Tasks":
    st.header("View All Tasks")
    tasks = retrieve_tasks()
    for task in tasks:
        st.write(f"ID: {task[0]}, Task: {task[1]}, Start: {task[2]}, Due: {task[3]}, Responsible: {task[4]}, Status: {task[5]}")
        if st.button(f"Delete Task {task[0]}", key=f"delete_{task[0]}"):
            delete_task(task[0])
            st.success("Task deleted!")
        if st.button(f"Edit Task {task[0]}", key=f"edit_{task[0]}"):
            st.session_state.edit_task = task

elif menu_option == "Reports":
    st.header("Task Reports")
    report_type = st.radio("Filter by", ["Status", "Responsible Person"])

    if report_type == "Status":
        status_filter = st.selectbox("Select Status", ["Not Started", "In-Progress", "Completed"])
        filtered_tasks = filter_tasks_by_status(status_filter)
        for task in filtered_tasks:
            st.write(f"ID: {task[0]}, Task: {task[1]}, Start: {task[2]}, Due: {task[3]}, Responsible: {task[4]}, Status: {task[5]}")

    elif report_type == "Responsible Person":
        person_filter = st.text_input("Enter Responsible Person Name")
        if st.button("Search"):
            filtered_tasks = filter_tasks_by_responsible_person(person_filter)
            for task in filtered_tasks:
                st.write(f"ID: {task[0]}, Task: {task[1]}, Start: {task[2]}, Due: {task[3]}, Responsible: {task[4]}, Status: {task[5]}")
st.text("")
st.text("Web Application made by Shamik Patel.\n Contact \n Email : 21BT04087@gsfcuniversity.ac.in , smpatel2353@gmail.com \n Mobile : 6353817643")
