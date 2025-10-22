import config
import json

with open(config.TASKMASTER_JSON_FILE, 'r') as task_master_file:
    tasks = json.loads(task_master_file.read())

task_list = tasks['master']['tasks']
with open("./task_list.md", "w") as task_list_file:
    for task in task_list:
        task_list_file.write(f"## {task['id']}. {task['title']}\n\n")
        task_list_file.write(f"{task['description']}\n\n")
        task_list_file.write(f"{task['details']}\n\n")
        task_list_file.write(f"**Test Strategy**: {task['testStrategy']}\n\n\n")
        task_list_file.write(f"### Subtasks\n\n")
        for subtask in task['subtasks']:
            task_list_file.write(f"#### {task['id']}.{subtask['id']} {subtask['title']}\n\n")
            task_list_file.write(f"{subtask['description']}\n\n")
            task_list_file.write(f"{subtask['details']}\n\n")
            task_list_file.write(f"**Test Strategy**: {subtask['testStrategy']}\n\n\n")


