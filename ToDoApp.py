import sqlite3

def create_connection(db_name):
    conn = sqlite3.connect(db_name)
    return conn

def create_table(conn):
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY,
                task TEXT,
                completed BOOLEAN
            )
        ''')

def add_task(conn, task):
    with conn:
        conn.execute("INSERT INTO todos (task, completed) VALUES (?, ?)", (task, False))

def list_tasks(conn):
    cursor = conn.execute("SELECT * FROM todos")
    tasks = cursor.fetchall()
    return tasks

def mark_task_completed(conn, task_id):
    with conn:
        conn.execute("UPDATE todos SET completed = ? WHERE id = ?", (True, task_id))

def delete_task(conn, task_id):
    with conn:
        conn.execute("DELETE FROM todos WHERE id = ?", (task_id,))

def main():
    conn = create_connection("todo.db")
    create_table(conn)

    while True:
        print("\nTo-Do List Application")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Mark Task Completed")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("Select an operation: ")

        if choice == "1":
            task = input("Enter the task: ")
            add_task(conn, task)
            print("Task added.")

        elif choice == "2":
            tasks = list_tasks(conn)
            if tasks:
                print("\nTask List:")
                for task in tasks:
                    task_id, task_text, completed = task
                    status = "Completed" if completed else "Not Completed"
                    print(f"Task ID: {task_id}, Task: {task_text}, Status: {status}")
            else:
                print("No tasks found.")

        elif choice == "3":
            task_id = input("Enter the task ID to mark as completed: ")
            mark_task_completed(conn, task_id)
            print("Task marked as completed.")

        elif choice == "4":
            task_id = input("Enter the task ID to delete: ")
            delete_task(conn, task_id)
            print("Task deleted.")

        elif choice == "5":
            conn.close()
            break

if __name__ == "__main__":
    main()