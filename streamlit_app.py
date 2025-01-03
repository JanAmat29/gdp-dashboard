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

# Inicialización de memoria
if "stored_data" not in st.session_state:
    st.session_state.stored_data = {}

# Función para guardar listas en memoria con descripción
def save_list_in_memory(list_type, data):
    timestamp = datetime.now().strftime("%d %b %Y (%H:%M)")
    if list_type == "names":
        description = f"{timestamp}: {', '.join([name[0] for name in data])}"
    elif list_type == "tasks":
        description = f"{timestamp}: {', '.join([f'{task[0]} ({task[1]})' for task in data])}"
    st.session_state.stored_data[description] = data

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
        save_list_in_memory("names", names)
    st.write("### Enter Tasks and Difficulty")
    task_input = st.text_area("Enter tasks in the format: task_name, difficulty (one per line):")
    if task_input:
        tasks = [[line.split(",")[0].strip(), int(line.split(",")[1])] for line in task_input.splitlines()]
        save_list_in_memory("tasks", tasks)

elif option == "Use existing lists of names and tasks":
    stored_names = {k: v for k, v in st.session_state.stored_data.items() if "names" in k}
    stored_tasks = {k: v for k, v in st.session_state.stored_data.items() if "tasks" in k}
    names_key = st.selectbox("Select a list of names:", list(stored_names.keys()))
    tasks_key = st.selectbox("Select a list of tasks:", list(stored_tasks.keys()))
    if names_key and tasks_key:
        names = stored_names[names_key]
        tasks = stored_tasks[tasks_key]

elif option == "Use existing names and create a list of tasks":
    stored_names = {k: v for k, v in st.session_state.stored_data.items() if "names" in k}
    names_key = st.selectbox("Select a list of names:", list(stored_names.keys()))
    if names_key:
        names = stored_names[names_key]
        st.write("### Enter Tasks and Difficulty")
        task_input = st.text_area("Enter tasks in the format: task_name, difficulty (one per line):")
        if task_input:
            tasks = [[line.split(",")[0].strip(), int(line.split(",")[1])] for line in task_input.splitlines()]
            save_list_in_memory("tasks", tasks)

elif option == "Use existing tasks and create a list of names":
    stored_tasks = {k: v for k, v in st.session_state.stored_data.items() if "tasks" in k}
    tasks_key = st.selectbox("Select a list of tasks:", list(stored_tasks.keys()))
    if tasks_key:
        tasks = stored_tasks[tasks_key]
        st.write("### Enter Names")
        name_input = st.text_area("Enter names (one per line):")
        if name_input:
            names = [[name] for name in name_input.splitlines()]
            save_list_in_memory("names", names)

if st.button("Organize Tasks"):
    if names and tasks:
        final_names, final_tasks = work_to_do(names, tasks)
        save_list_in_memory("names", final_names)
        save_list_in_memory("tasks", final_tasks)
    else:
        st.write("Please provide both names and tasks.")
