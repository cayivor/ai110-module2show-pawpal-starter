import streamlit as st

# 1. ALWAYS FIRST: Page config must run before any other Streamlit commands
st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

from pawpal_system import Scheduler, Owner, Pet, Task

# 2. Manage Application Memory
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

if "owner" not in st.session_state:
    default_owner = Owner(name="Chelsea")
    st.session_state.owner = default_owner
    st.session_state.scheduler.register_owner(default_owner)

# --- UI Header ---
st.title("🐾 PawPal+")

st.markdown(
    """
    Welcome to your interactive PawPal+ care planning dashboard! 
    Use the controls below to register pets, assign their daily tasks, and generate an aggregated schedule.
    """
)

with st.expander("Scenario & Requirements", expanded=False):
    st.markdown(
        """
        **PawPal+** helps a pet owner plan care tasks based on constraints like time, priority, and preferences.
        - Represent pet care tasks (what needs to happen, frequency, completion status)
        - Represent the pet and the owner
        - Build an aggregated daily schedule plan
        """
    )

st.divider()

# --- Section 1: Profile Setup ---
st.subheader("👤 Profile & Pet Registration")

# Dynamically sync Owner name with our backend object
owner_name_input = st.text_input("Owner Name", value=st.session_state.owner.name)
st.session_state.owner.name = owner_name_input

col_p1, col_p2 = st.columns(2)
with col_p1:
    reg_pet_name = st.text_input("Pet Name", value="Mochi")
with col_p2:
    reg_species = st.selectbox("Species", ["Dog", "Cat", "Other"])

if st.button("🐾 Register / Add Pet"):
    # Check if pet already exists to avoid duplicates
    existing_pet_names = [p.name.lower() for p in st.session_state.owner.get_all_pets()]
    if reg_pet_name.lower() in existing_pet_names:
        st.warning(f"'{reg_pet_name}' is already registered!")
    elif reg_pet_name.strip() == "":
        st.error("Pet name cannot be empty.")
    else:
        new_pet = Pet(name=reg_pet_name, species=reg_species)
        st.session_state.owner.add_pet(new_pet)
        st.success(f"Successfully registered {new_pet.name} the {new_pet.species}!")

# Display current registered pets
current_pets = st.session_state.owner.get_all_pets()
if current_pets:
    pet_list_str = ", ".join([f"**{p.name}** ({p.species})" for p in current_pets])
    st.markdown(f"**Registered Pets:** {pet_list_str}")
else:
    st.info("No pets registered yet. Register a pet above so you can assign tasks to them!")

st.divider()

# --- Section 2: Task Management ---
st.subheader("📋 Task Manager")

# Dropdown to choose WHICH registered pet gets the task
if current_pets:
    selected_pet_name = st.selectbox("Assign Task To:", [p.name for p in current_pets])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task Title", value="Morning walk")
    with col2:
        due_time = st.text_input("Due Time", value="08:00 AM")
    with col3:
        frequency = st.selectbox("Frequency", ["Once", "Daily", "Weekly"])

    if st.button("➕ Add Task"):
        # Match name to find our backend Pet object
        target_pet = next((p for p in current_pets if p.name == selected_pet_name), None)
        
        if target_pet:
            new_task = Task(description=task_title, due_time=due_time, frequency=frequency)
            target_pet.add_task(new_task)
            st.success(f"Added '{task_title}' to {target_pet.name}'s schedule!")
else:
    st.warning("⚠️ Please register at least one pet above to unlock the Task Manager.")

# --- Section 3: Schedule Generation ---
st.divider()
st.subheader("🗓️ Daily Planner")
st.caption("Click below to compile all pending pet activities into a single timeline.")

if st.button("⚡ Generate Schedule"):
    daily_schedule = st.session_state.scheduler.get_daily_schedule(st.session_state.owner)
    
    if not daily_schedule:
        st.info("🎉 All clear! No pending tasks for your pets today.")
    else:
        st.markdown(f"### Today's Schedule for {st.session_state.owner.name}'s Household")
        for item in daily_schedule:
            p_name = item["pet_name"]
            t_obj = item["task"]
            st.info(f"⏰ **[{t_obj.due_time}]** — **{p_name}**: {t_obj.description} *({t_obj.frequency})*")