import argparse
import json
from pathlib import Path

# Define the paths to the JSON and .txt files
DATA_FILE = Path("tasks.json")
TEXT_FILE = Path("C:/Users/jcbra/101_files/todo_list.txt")

# Function to load tasks from JSON or .txt file
def load_tasks():
    if DATA_FILE.exists():
        # Load tasks from the JSON file
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        # If tasks.json doesn't exist, load tasks from the .txt file
        return load_tasks_from_txt()

# Function to load tasks from the .txt file and convert to a dictionary
def load_tasks_from_txt():
    tasks = {}
    if TEXT_FILE.exists():
        with open(TEXT_FILE, "r", encoding='utf-8') as f:
            for i, line in enumerate(f, start=1):
                line = line.strip()
                if " - " in line:
                    name, status = line.split(" - ")
                    tasks[str(i)] = {"name": name, "status": status}
                else:
                    tasks[str(i)] = {"name": line, "status": "not done"}
    save_tasks(tasks)  # Save the loaded tasks to JSON for future use
    return tasks

# Save tasks to the JSON file
def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding='utf-8') as f:
        json.dump(tasks, f, indent=4)

# Add a new task
def add_task(tasks, task_name):
    task_id = str(len(tasks) + 1)
    tasks[task_id] = {"name": task_name, "status": "not done"}
    save_tasks(tasks)
    print(f"Added task: {task_name}")

# Update an existing task
def update_task(tasks, task_id, new_name):
    if task_id in tasks:
        tasks[task_id]["name"] = new_name
        save_tasks(tasks)
        print(f"Updated task {task_id} to: {new_name}")
    else:
        print(f"Task {task_id} not found.")

# Delete a task
def delete_task(tasks, task_id):
    if task_id in tasks:
        del tasks[task_id]
        save_tasks(tasks)
        print(f"Deleted task {task_id}.")
    else:
        print(f"Task {task_id} not found.")

# Mark a task as in progress
def mark_in_progress(tasks, task_id):
    if task_id in tasks:
        tasks[task_id]["status"] = "in progress"
        save_tasks(tasks)
        print(f"Task {task_id} marked as in progress.")
    else:
        print(f"Task {task_id} not found.")

# Mark a task as done
def mark_done(tasks, task_id):
    if task_id in tasks:
        tasks[task_id]["status"] = "done"
        save_tasks(tasks)
        print(f"Task {task_id} marked as done.")
    else:
        print(f"Task {task_id} not found.")

# List all tasks
def list_tasks(tasks):
    if tasks:
        for task_id, task in tasks.items():
            print(f"{task_id}: {task['name']} [{task['status']}]")
    else:
        print("No tasks found.")

# List tasks by their status
def list_tasks_by_status(tasks, status):
    filtered_tasks = {k: v for k, v in tasks.items() if v["status"] == status}
    if filtered_tasks:
        for task_id, task in filtered_tasks.items():
            print(f"{task_id}: {task['name']} [{task['status']}]")
    else:
        print(f"No tasks with status '{status}' found.")

# Main function to handle command line arguments
def main():
    parser = argparse.ArgumentParser(description="Task Manager")
    
    parser.add_argument("action", help="Action to perform: add, update, delete, mark_in_progress, mark_done, list, list_done, list_not_done, list_in_progress")
    parser.add_argument("--task", help="Task name for adding or updating")
    parser.add_argument("--task_id", help="Task ID for updating, deleting, or marking as done/in progress")
    
    args = parser.parse_args()

    # Load tasks from the JSON or .txt file
    tasks = load_tasks()

    # Handle user actions
    if args.action == "add" and args.task:
        add_task(tasks, args.task)
    elif args.action == "update" and args.task_id and args.task:
        update_task(tasks, args.task_id, args.task)
    elif args.action == "delete" and args.task_id:
        delete_task(tasks, args.task_id)
    elif args.action == "mark_in_progress" and args.task_id:
        mark_in_progress(tasks, args.task_id)
    elif args.action == "mark_done" and args.task_id:
        mark_done(tasks, args.task_id)
    elif args.action == "list":
        list_tasks(tasks)
    elif args.action == "list_done":
        list_tasks_by_status(tasks, "done")
    elif args.action == "list_not_done":
        list_tasks_by_status(tasks, "not done")
    elif args.action == "list_in_progress":
        list_tasks_by_status(tasks, "in progress")
    else:
        print("Invalid command or missing arguments.")

if __name__ == "__main__":
    main()
