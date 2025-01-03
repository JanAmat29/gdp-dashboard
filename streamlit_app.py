import streamlit as st
from random import randint

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

def process_input_as_list(user_input):
    try:
        return eval(user_input) if isinstance(eval(user_input), list) else []
    except:
        return []

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

elif option == "Use existing lists of names and tasks":
    names = process_input_as_list(st.text_input("Enter the list of names (as a Python list):"))
    tasks = process_input_as_list(st.text_input("Enter the list of tasks (as a Python list of [task_name, difficulty]):"))

elif option == "Use existing names and create a list of tasks":
    names = process_input_as_list(st.text_input("Enter the list of names (as a Python list):"))
    st.write("### Enter Tasks and Difficulty")
    task_input = st.text_area("Enter tasks in the format: task_name, difficulty (one per line):")
    if task_input:
        tasks = [[line.split(",")[0].strip(), int(line.split(",")[1])] for line in task_input.splitlines()]

elif option == "Use existing tasks and create a list of names":
    tasks = process_input_as_list(st.text_input("Enter the list of tasks (as a Python list of [task_name, difficulty]):"))
    st.write("### Enter Names")
    name_input = st.text_area("Enter names (one per line):")
    if name_input:
        names = [[name] for name in name_input.splitlines()]

if st.button("Organize Tasks"):
    if names and tasks:
        work_to_do(names, tasks)
    else:
        st.write("Please provide both names and tasks.")
