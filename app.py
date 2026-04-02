import streamlit as st
import pandas as pd

from pawpal_system import Task, Pet, Owner, Scheduler
from helper_functions import no_pet_duplicates, get_first_pet_duplicate, create_pet_dataframe
from datetime import timedelta

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner and Pets")

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

# Block handles adding a new owner
if "owner" not in st.session_state:
    st.session_state.owner = None
if owner_name := st.text_input("Owner name", value="Jordan"):
    if st.session_state.owner == None or owner_name != st.session_state.owner.name:
        owner = Owner(owner_name)
        st.session_state.owner = owner
        st.session_state.pet = None # Reset current pet(s) when new owner is added
        st.session_state.scheduler.add_owner(owner)
if st.session_state.owner:
    st.text(f"Current owner: {st.session_state.owner.name}")
else:
    st.info("No owner yet. Add one above.")

# Block handles adding a new pet
col7, col8, col9 = st.columns(3)
with col7:
    pet_name = st.text_input("Pet name", value="Mochi")
with col8:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col9:
    age = st.number_input("Age", min_value=0, value = 0)

if "pet" not in st.session_state:
    st.session_state.pet = None
if st.button("Add Pet"):
    # If no pet with matching details exists, create one
    if st.session_state.owner == None:
        st.info("No owner selected yet to associate with pet. Add one above.")
    else:
        # Check if values match for any pet associated with the owner
        pet_to_add = Pet(pet_name, species, age)
        if no_pet_duplicates(pet_to_add, st.session_state.owner.pets):
            st.session_state.pet = pet_to_add
            st.session_state.owner.add_pet(pet_to_add)
        else:
            st.session_state.pet = get_first_pet_duplicate(pet_to_add, st.session_state.owner.pets)
if st.session_state.pet:
    st.text(f"Current pet: {st.session_state.pet.name}, the {st.session_state.pet.age} year old {st.session_state.pet.species}.")
    st.table(create_pet_dataframe(st.session_state.owner.pets))
else:
    st.info("No pet selected yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

# Row 1
col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

# Row 2
col4, col5, col6 = st.columns(3)
with col4:
    task_date = st.date_input("Date", value="today")
with col5:
    task_scheduled_time = st.time_input("Time", value="now")
with col6:
    task_frequency = st.selectbox("Frequency", ["once", "daily", "weekly"], index=0)

if st.button("Add task"):
    if st.session_state.pet:
        st.session_state.pet.add_task(Task(
            task_title,
            task_date,
            task_scheduled_time,
            task_frequency,
            timedelta(duration),
            priority
        ))
    else:
        st.info("No pets associated with owner yet. Add one above.")
if st.session_state.owner:
    owner_tasks = st.session_state.owner.get_all_tasks()
    if owner_tasks:
        st.write("Current tasks:")
        st.table(st.session_state.owner.get_all_tasks())
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    conflicts = st.session_state.scheduler.detect_task_conflicts()
    if not conflicts:
        st.success("No conflicts detected in schedule")
    else:
        st.warning(f"Schedule conflicts detected")
        df = pd.DataFrame([
            {
                "Pet": pet.name,
                "First task": t1.description,
                "Second task": t2.description
            } for pet, t1, t2 in conflicts
        ])
        st.table(df)
    pet_task_associations = st.session_state.scheduler.organize_tasks_for_date()
    if pet_task_associations:
        df = pd.DataFrame([
            {
                "Pet": pet.name,
                "Description": t.description,
                "Date": t.date,
                "Time": t.scheduled_time,
                "Frequency": t.frequency,
                "Duration": t.duration,
                "Priority": t.priority,
            }
            for pet, t in pet_task_associations
        ])
        st.table(df)
    else:
        st.warning(f"No tasks to display")
#     st.warning(
#         "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
#     )
#     st.markdown(
#         """
# Suggested approach:
# 1. Design your UML (draft).
# 2. Create class stubs (no logic).
# 3. Implement scheduling behavior.
# 4. Connect your scheduler here and display results.
# """
#     )
