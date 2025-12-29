import pandas as pd
from datetime import datetime

tasks = []

def add_task(title, description, priority, deadline):
    task_id = len(tasks) + 1
    task = {
        'task_id': task_id,
        'title': title,
        'description': description,
        'priority': priority,
        'deadline': deadline,
        'status': False
    }
    tasks.append(task)
    print("Task added successfully.")


def show_task_list():
    if len(tasks) == 0:
        print("No tasks available.")
        return
    print("\nCurrent Tasks:")
    for task in tasks:
        status = "Completed" if task['status'] else "Pending"
        print(f"ID: {task['task_id']} | {task['title']} | {status}")


def update_task(task_id, title=None, description=None, priority=None, deadline=None):
    found = False
    for task in tasks:
        if task['task_id'] == task_id:
            if title: task['title'] = title
            if description: task['description'] = description
            if priority is not None: task['priority'] = priority
            if deadline: task['deadline'] = deadline
            found = True
            print("Task updated successfully.")
            break
    if not found:
        print("Task ID not found.")


def delete_task(task_id):
    global tasks
    new_tasks = [t for t in tasks if t['task_id'] != task_id]
    if len(new_tasks) == len(tasks):
        print("Task ID not found.")
        return
    tasks[:] = new_tasks
    for i, t in enumerate(tasks): t['task_id'] = i + 1
    print("Task deleted successfully.")


def mark_completed(task_id):
    for task in tasks:
        if task['task_id'] == task_id:
            task['status'] = True
            print("Task marked as completed.")
            return
    print("Task ID not found.")


def get_dataframe():
    if len(tasks) == 0:
        return pd.DataFrame()
    df = pd.DataFrame(tasks)
    df['deadline'] = pd.to_datetime(df['deadline'], dayfirst=True)
    df['status'] = df['status'].apply(lambda x: "Completed" if x else "Pending")
    return df


def view_tasks(sort_by='priority'):
    df = get_dataframe()
    if df.empty:
        print("No tasks available.")
        return
    df = df.sort_values(by=['priority','deadline']) if sort_by=='priority' else df.sort_values(by=['deadline','priority'])
    print(df[['task_id','title','priority','deadline','status']].to_string(index=False))


def progress_stats():
    df = get_dataframe()
    if df.empty:
        print("No tasks available.")
        return

    total = df.shape[0]
    completed = sum(df['status']=="Completed")

    print("\n--- Progress Overview ---")
    print(df[['task_id','title','status']].to_string(index=False))
    print(f"\nTotal Tasks: {total}")
    print(f"Completed: {completed}")
    print("Progress: {:.2f}%".format(completed/total*100))


def get_schedule(period='daily'):
    df = get_dataframe()
    if df.empty:
        print("No tasks available.")
        return
    today = pd.Timestamp(datetime.now().date())
    if period == 'daily':
        schedule = df[(df['deadline']==today) & (df['status']=="Pending")]
        print(f"Tasks for Today ({today.date()}):")
    else:
        week_end = today + pd.Timedelta(days=7)
        schedule = df[(df['deadline']>=today) & (df['deadline']<=week_end) & (df['status']=="Pending")]
        print(f"Tasks for This Week ({today.date()} to {week_end.date()}):")

    if schedule.empty:
        print("No tasks scheduled.")
        return
    print(schedule[['task_id','title','priority','deadline','status']].to_string(index=False))


def input_date():
    while True:
        date_in = input("Enter Deadline (DD-MM-YYYY): ").strip()
        try:
            datetime.strptime(date_in, "%d-%m-%Y")
            return date_in
        except:
            print("Invalid format! Please enter as DD-MM-YYYY.")


def main_menu():
    while True:
        print("\n--- Smart Task Scheduler Menu ---")
        print("1. Add Task")
        print("2. Update Task")
        print("3. Delete Task")
        print("4. View Tasks Sorted by Priority")
        print("5. View Tasks Sorted by Deadline")
        print("6. Mark Task as Completed")
        print("7. View Progress")
        print("8. Get Daily Schedule")
        print("9. Get Weekly Schedule")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            title = input("Enter Title: ").strip()
            desc = input("Enter Description: ").strip()
            priority = int(input("Enter Priority (1=High, 5=Low): "))
            deadline = input_date()
            add_task(title, desc, priority, deadline)

        elif choice in ['2','3','6']:
            show_task_list()
            try: task_id = int(input("Enter Task ID: "))
            except: print("Invalid ID"); continue
            if choice=='2':
                print("Leave empty to skip")
                title = input("New Title: ").strip() or None
                desc = input("New Description: ").strip() or None
                p = input("New Priority (1-5): ").strip(); pr = int(p) if p else None
                deadline = input_date() if input("Change deadline? (y/n): ").lower()=="y" else None
                update_task(task_id, title, desc, pr, deadline)
            elif choice=='3': delete_task(task_id)
            else: mark_completed(task_id)

        elif choice == '4': view_tasks('priority')
        elif choice == '5': view_tasks('deadline')
        elif choice == '7': progress_stats()
        elif choice == '8': get_schedule('daily')
        elif choice == '9': get_schedule('weekly')
        elif choice == '0': print("Goodbye!"); break
        else: print("Invalid choice.")

if __name__ == "__main__":
    main_menu()
