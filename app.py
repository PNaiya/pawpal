import streamlit as st
from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler


st.set_page_config(page_title="PawPal+", layout="wide")
st.title("PawPal+ Smart Pet Care Manager")

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Alex")

owner = st.session_state.owner
scheduler = Scheduler(owner)

st.header("Add a Pet")
with st.form("add_pet_form"):
    pet_name = st.text_input("Pet Name")
    pet_species = st.text_input("Species")
    pet_age = st.number_input("Age", min_value=0, step=1)
    submitted_pet = st.form_submit_button("Add Pet")

    if submitted_pet:
        if pet_name and pet_species:
            owner.add_pet(Pet(pet_name, pet_species, int(pet_age)))
            st.success(f"{pet_name} added successfully.")
        else:
            st.warning("Please fill in all pet fields.")

st.header("Schedule a Task")
pet_names = [pet.name for pet in owner.pets]

if pet_names:
    with st.form("task_form"):
        selected_pet = st.selectbox("Choose Pet", pet_names)
        description = st.text_input("Task Description")
        time_value = st.text_input("Time (HH:MM)", value="08:00")
        task_date = st.date_input("Date", value=date.today())
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        submitted_task = st.form_submit_button("Add Task")

        if submitted_task:
            pet = owner.get_pet(selected_pet)
            if pet and description and time_value:
                pet.add_task(Task(description, time_value, task_date, frequency))
                st.success(f"Task added for {selected_pet}.")
            else:
                st.warning("Please complete all task fields.")
else:
    st.info("Add a pet first to schedule tasks.")

st.header("Today's Schedule")
today_tasks = scheduler.sort_by_time(scheduler.get_todays_tasks())

if today_tasks:
    display_rows = []
    for task in today_tasks:
        display_rows.append({
            "Time": task.time,
            "Pet": task.pet_name,
            "Task": task.description,
            "Frequency": task.frequency,
            "Completed": task.completed
        })
    st.table(display_rows)

    conflicts = scheduler.detect_conflicts(today_tasks)
    for warning in conflicts:
        st.warning(warning)
else:
    st.write("No tasks scheduled for today.")

st.header("Mark Task Complete")
incomplete_tasks = [task for task in owner.get_all_tasks() if not task.completed]

if incomplete_tasks:
    labels = [
        f"{task.pet_name} - {task.description} at {task.time} on {task.date}"
        for task in incomplete_tasks
    ]

    selected_label = st.selectbox("Choose a task", labels)
    selected_index = labels.index(selected_label)
    selected_task = incomplete_tasks[selected_index]

    if st.button("Mark Complete"):
        new_task = scheduler.mark_task_complete(selected_task)
        st.success("Task marked complete.")
        if new_task:
            st.info(f"Recurring task rescheduled for {new_task.date} at {new_task.time}.")
        st.rerun()
else:
    st.write("No incomplete tasks available.")