#Project Title : Task Management System
#Enrollment No. : 23002171210075
#Subject name : Python
#Date : 28-02-25

import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Task Management System")
        self.root.geometry("500x600")

        self.task_listbox = tk.Listbox(self.root)
        self.tasks = []
        self.deleted_tasks = []  # To implement undo feature

        # Load tasks from file on startup
        self.load_tasks()

        # Create UI components
        self.create_widgets()

    def create_widgets(self):
        # Entry widget for task input
        self.task_entry = tk.Entry(self.root, width=40)
        self.task_entry.pack(pady=10)

        # Buttons for actions
        self.add_button = tk.Button(self.root, text="Add Task", width=20, command=self.add_task)
        self.add_button.pack(pady=5)

        self.edit_button = tk.Button(self.root, text="Edit Task", width=20, command=self.edit_task)
        self.edit_button.pack(pady=5)

        self.task_listbox = tk.Listbox(self.root, height=12, width=40, selectmode=tk.SINGLE)
        self.task_listbox.pack(pady=10)

        self.delete_button = tk.Button(self.root, text="Delete Task", width=20, command=self.delete_task)
        self.delete_button.pack(pady=5)

        self.complete_button = tk.Button(self.root, text="Mark as Completed", width=20, command=self.mark_completed)
        self.complete_button.pack(pady=5)

        self.clear_button = tk.Button(self.root, text="Clear All Tasks", width=20, command=self.clear_all_tasks)
        self.clear_button.pack(pady=5)

        self.undo_button = tk.Button(self.root, text="Undo Last Operation", width=20, command=self.undo_last_operation)
        self.undo_button.pack(pady=5)

        self.search_button = tk.Button(self.root, text="Search Task", width=20, command=self.search_task)
        self.search_button.pack(pady=5)

        self.filter_button = tk.Button(self.root, text="Filter Incomplete Tasks", width=20, command=self.filter_incomplete_tasks)
        self.filter_button.pack(pady=5)

    def add_task(self):
        task = self.task_entry.get()
        if task:
            task_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current date and time
            task_with_date = f"{task} - Created on: {task_date}"
            self.tasks.append({'task': task, 'created_on': task_date})
            self.task_listbox.insert(tk.END, task_with_date)
            self.task_entry.delete(0, tk.END)
            self.save_tasks()
        else:
            messagebox.showwarning("Input Error", "Please enter a task.")

    def delete_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            task = self.tasks[selected_task_index]
            creation_time = datetime.strptime(task['created_on'], "%Y-%m-%d %H:%M:%S")  # Convert string to datetime
            current_time = datetime.now()
            time_diff = current_time - creation_time  # Calculate time difference
            days = time_diff.days
            hours, remainder = divmod(time_diff.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            # Store the task for undo
            self.deleted_tasks.append(('delete', selected_task_index, task))

            # Display the time difference
            messagebox.showinfo("Task Deleted", f"Task '{task['task']}' deleted.\n"
                                              f"Time taken: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds")

            # Delete the task
            self.task_listbox.delete(selected_task_index)
            self.tasks.pop(selected_task_index)
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def mark_completed(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            task = self.tasks[selected_task_index]
            self.tasks[selected_task_index]['task'] = f"{task['task']} (Completed)"
            self.task_listbox.delete(selected_task_index)
            self.task_listbox.insert(selected_task_index, f"{task['task']} (Completed)")
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")

    def edit_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            new_task = self.task_entry.get()
            if new_task:
                old_task = self.tasks[selected_task_index]['task']
                task_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Update date when editing
                new_task_with_date = f"{new_task} - Created on: {task_date}"
                self.tasks[selected_task_index] = {'task': new_task, 'created_on': task_date}
                self.deleted_tasks.append(('edit', selected_task_index, old_task))  # Store for undo
                self.task_listbox.delete(selected_task_index)
                self.task_listbox.insert(selected_task_index, new_task_with_date)
                self.task_entry.delete(0, tk.END)
                self.save_tasks()
            else:
                messagebox.showwarning("Input Error", "Please enter a new task.")
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to edit.")

    def clear_all_tasks(self):
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks?")
        if confirm:
            self.deleted_tasks.extend([('delete', i, task) for i, task in enumerate(self.tasks)])
            self.task_listbox.delete(0, tk.END)
            self.tasks.clear()
            self.save_tasks()

    def undo_last_operation(self):
        if not self.deleted_tasks:
            messagebox.showinfo("Undo Error", "No operations to undo.")
            return
        last_operation = self.deleted_tasks.pop()
        if last_operation[0] == 'delete':
            task = last_operation[2]
            index = last_operation[1]
            self.tasks.insert(index, task)
            self.task_listbox.insert(index, f"{task['task']} - Created on: {task['created_on']}")
        elif last_operation[0] == 'edit':
            old_task = last_operation[2]
            index = last_operation[1]
            self.tasks[index] = old_task
            self.task_listbox.delete(index)
            self.task_listbox.insert(index, old_task)
        self.save_tasks()

    def search_task(self):
        search_term = self.task_entry.get().lower()
        matching_tasks = [task['task'] for task in self.tasks if search_term in task['task'].lower()]
        self.task_listbox.delete(0, tk.END)
        for task in matching_tasks:
            self.task_listbox.insert(tk.END, task)

    def filter_incomplete_tasks(self):
        self.task_listbox.delete(0, tk.END)
        incomplete_tasks = [task['task'] for task in self.tasks if "(Completed)" not in task['task']]
        for task in incomplete_tasks:
            self.task_listbox.insert(tk.END, task)

    def load_tasks(self):
        if os.path.exists("tasks.txt"):
            with open("tasks.txt", "r") as file:
                loaded_tasks = file.readlines()
                for task in loaded_tasks:
                    task_desc, created_on = task.strip().rsplit(' - Created on: ', 1)
                    self.tasks.append({'task': task_desc, 'created_on': created_on})
                    self.task_listbox.insert(tk.END, f"{task_desc} - Created on: {created_on}")

    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            for task in self.tasks:
                file.write(f"{task['task']} - Created on: {task['created_on']}\n")


# Main function to initialize the Tkinter window
def main():
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()