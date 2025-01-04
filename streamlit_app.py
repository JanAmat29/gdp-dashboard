import streamlit as st
from random import randint
from datetime import datetime

# Función para organizar tareas
# Actualizar la visualización de las tareas asignadas a cada persona
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
        for idx, task in enumerate(name[1:], start=1):
            st.write(f"  {idx}. {task}")

    st.write("\n### Difficulty per person:")
    for name in names:
        total_dif_tasks = sum(task[1] for task in tasks if task[0] in name[1:])
        num_tasks = len(name) - 1
        avg_difficulty = round(total_dif_tasks / num_tasks, 2) if num_tasks > 0 else 0
        st.write(f"{name[0]}: {avg_difficulty}")

    return names, tasks


# Función para formatear listas guardadas (nombres)
def format_saved_names(key, data):
    date_str = datetime.strptime(key, "%Y-%m-%d %H:%M:%S").strftime("%d %b %Y (%H:%M)")
    formatted = f"{date_str}: {', '.join([name[0] for name in data])}"
    return formatted

# Función para formatear listas guardadas (tareas)
def format_saved_tasks(key, data):
    date_str = datetime.strptime(key, "%Y-%m-%d %H:%M:%S").strftime("%d %b %Y (%H:%M)")
    formatted = f"{date_str}: {', '.join([f'{task[0]} ({task[1]})' for task in data])}"
    return formatted

# Inicialización de memoria
if "stored_data" not in st.session_state:
    st.session_state.stored_data = {}

# Streamlit UI
st.title("Task To Do")
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

elif option == "Use existing lists of names and tasks":
    st.write("### Choose saved names and tasks separately")
    if st.session_state.stored_data:
        saved_keys = list(st.session_state.stored_data.keys())

        # Nombres
        formatted_names_options = [
            format_saved_names(key, st.session_state.stored_data[key][0])
            for key in saved_keys
        ]
        chosen_names_option = st.selectbox("Select a saved list of names:", options=formatted_names_options)
        chosen_names_key = saved_keys[formatted_names_options.index(chosen_names_option)]
        names = st.session_state.stored_data[chosen_names_key][0]

        # Tareas
        formatted_tasks_options = [
            format_saved_tasks(key, st.session_state.stored_data[key][1])
            for key in saved_keys
        ]
        chosen_tasks_option = st.selectbox("Select a saved list of tasks:", options=formatted_tasks_options)
        chosen_tasks_key = saved_keys[formatted_tasks_options.index(chosen_tasks_option)]
        tasks = st.session_state.stored_data[chosen_tasks_key][1]

        st.write("### Selected Names and Tasks:")
        st.write(f"Names: {', '.join([name[0] for name in names])}")
        st.write(f"Tasks: {', '.join([f'{task[0]} ({task[1]})' for task in tasks])}")

        if st.button("Organize Tasks"):
            final_names, final_tasks = work_to_do(names, tasks)
            st.session_state.stored_data[datetime.now().strftime("%Y-%m-%d %H:%M:%S")] = (final_names, final_tasks)

elif option == "Use existing names and create a list of tasks":
    st.write("### Choose saved names")
    if st.session_state.stored_data:
        saved_keys = list(st.session_state.stored_data.keys())

        formatted_names_options = [
            format_saved_names(key, st.session_state.stored_data[key][0])
            for key in saved_keys
        ]
        chosen_names_option = st.selectbox("Select a saved list of names:", options=formatted_names_options)
        chosen_names_key = saved_keys[formatted_names_options.index(chosen_names_option)]
        names = st.session_state.stored_data[chosen_names_key][0]

        st.write("### Enter Tasks and Difficulty")
        task_input = st.text_area("Enter tasks in the format: task_name, difficulty (one per line):")
        if task_input:
            tasks = [[line.split(",")[0].strip(), int(line.split(",")[1])] for line in task_input.splitlines()]
        if st.button("Organize Tasks"):
            final_names, final_tasks = work_to_do(names, tasks)
            st.session_state.stored_data[datetime.now().strftime("%Y-%m-%d %H:%M:%S")] = (final_names, final_tasks)
    else:
        st.write("No saved data available.")

elif option == "Use existing tasks and create a list of names":
    st.write("### Choose saved tasks")
    if st.session_state.stored_data:
        saved_keys = list(st.session_state.stored_data.keys())

        formatted_tasks_options = [
            format_saved_tasks(key, st.session_state.stored_data[key][1])
            for key in saved_keys
        ]
        chosen_tasks_option = st.selectbox("Select a saved list of tasks:", options=formatted_tasks_options)
        chosen_tasks_key = saved_keys[formatted_tasks_options.index(chosen_tasks_option)]
        tasks = st.session_state.stored_data[chosen_tasks_key][1]

        st.write("### Enter Names")
        name_input = st.text_area("Enter names (one per line):")
        if name_input:
            names = [[name] for name in name_input.splitlines()]
        if st.button("Organize Tasks"):
            final_names, final_tasks = work_to_do(names, tasks)
            st.session_state.stored_data[datetime.now().strftime("%Y-%m-%d %H:%M:%S")] = (final_names, final_tasks)
    else:
        st.write("No saved data available.")
