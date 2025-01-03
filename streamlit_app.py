import streamlit as st
from random import randint
from datetime import datetime

# Función para organizar tareas
def work_to_do(names, tasks):
    for dif in reversed(range(1, 4)):
        for j in range(len(tasks)):
            if tasks[j][1] == dif:
                task_counts = [len(names[y]) - 1 for y in range(len(names))]
                all_equal = all(count == task_counts[0] for count in task_counts)

                if all_equal:
                    who = randint(0, len(names) - 1)
                else:
                    len_min = float('inf')
                    who = 0
                    for y in range(len(names)):
                        if len(names[y]) - 1 < len_min:
                            len_min = len(names[y]) - 1
                            who = y

                names[who].append(tasks[j][0])

    st.write("### Tasks Organized Are:")
    for name in names:
        st.write(f"{name[0]} has to:")
        st.write(", ".join(name[1:]))

    st.write("\n### Difficulty per person:")
    for name in names:
        total_dif_tasks = sum(task[1] for task in tasks if task[0] in name[1:])
        num_tasks = len(name) - 1
        avg_difficulty = round(total_dif_tasks / num_tasks, 2) if num_tasks > 0 else 0
        st.write(f"{name[0]}: {avg_difficulty}")

    return names, tasks

# Función para formatear las listas guardadas
def format_saved_list(key, data):
    date_str = datetime.strptime(key, "%Y-%m-%d %H:%M:%S").strftime("%d %b %Y (%H:%M)")
    if isinstance(data[0][0], list):  # Si son nombres
        formatted = f"{date_str}: {', '.join([name[0] for name in data])}"
    else:  # Si son tareas
        formatted = f"{date_str}: {', '.join([f'{task[0]} ({task[1]})' for task in data])}"
    return formatted

# Inicialización de memoria
if "stored_data" not in st.session_state:
    st.session_state.stored_data = {}

# Streamlit UI
st.title("Task Organizer")
st.write("Organize tasks efficiently among people.")

option = st.radio(
    "Choose your option:",
    (
        "Create a list of names and tasks",
        "Use existing lists of names and tasks",
        "Use existing names and create a list of tasks",
        "Use existing tasks and create a list of names",
    )
)

names = []
tasks = []

if option == "Create a list of names and tasks":
    st.write("### Enter Names")
    name_input = st.text_area("Enter names (one per line):")
    if name_input:
        names = [[name] for name in name_input.splitlines()]
    st.write("### Enter Tasks and Difficulty")
    task_input = st.text_area("Enter tasks in the format: task_name, difficulty (one per line):")
    if task_input:
        tasks = [[line.split(",")[0].strip(), int(line.split(",")[1])] for line in task_input.splitlines()]
    if st.button("Organize Tasks"):
        if names and tasks:
            final_names, final_tasks = work_to_do(names, tasks)
            st.session_state.stored_data[datetime.now().strftime("%Y-%m-%d %H:%M:%S")] = (final_names, final_tasks)
        else:
            st.write("Please provide both names and tasks.")

else:
    st.write("### Choose a saved list")
    if st.session_state.stored_data:
        saved_keys = list(st.session_state.stored_data.keys())
        formatted_options = [
            format_saved_list(key, st.session_state.stored_data[key][0] if option != "Use existing tasks and create a list of names" else st.session_state.stored_data[key][1])
            for key in saved_keys
        ]

        chosen_option = st.selectbox("Select a saved list:", options=formatted_options)
        chosen_key = saved_keys[formatted_options.index(chosen_option)]

        if option == "Use existing lists of names and tasks":
            names, tasks = st.session_state.stored_data[chosen_key]
            st.write(f"Using names and tasks from: {chosen_option}")
        elif option == "Use existing names and create a list of tasks":
            names = st.session_state.stored_data[chosen_key][0]
            st.write("### Enter Tasks and Difficulty")
            task_input = st.text_area("Enter tasks in the format: task_name, difficulty (one per line):")
            if task_input:
                tasks = [[line.split(",")[0].strip(), int(line.split(",")[1])] for line in task_input.splitlines()]
            if st.button("Organize Tasks"):
                final_names, final_tasks = work_to_do(names, tasks)
                st.session_state.stored_data[datetime.now().strftime("%Y-%m-%d %H:%M:%S")] = (final_names, final_tasks)
        elif option == "Use existing tasks and create a list of names":
            tasks = st.session_state.stored_data[chosen_key][1]
            st.write("### Enter Names")
            name_input = st.text_area("Enter names (one per line):")
            if name_input:
                names = [[name] for name in name_input.splitlines()]
            if st.button("Organize Tasks"):
                final_names, final_tasks = work_to_do(names, tasks)
                st.session_state.stored_data[datetime.now().strftime("%Y-%m-%d %H:%M:%S")] = (final_names, final_tasks)
    else:
        st.write("No saved data available.")
