import tkinter as tk
from tkinter import messagebox
import logging
import os

# File handler and stream handler setup
logger = logging.getLogger("Task_Manager_Logger")
logger.setLevel(logging.DEBUG)

if logger.hasHandlers():
    logger.handlers.clear()

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)  
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler("task_manager.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Management App")
        self.root.geometry("400x500")
        self.tasks = []

        self.task_entry = tk.Entry(root, font=("Helvetica", 14))
        self.task_entry.pack(pady=10)

        self.task_listbox = tk.Listbox(root, font=("Helvetica", 14), height=15)
        self.task_listbox.pack(pady=10)

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add", width=10, command=self.add_task).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Update", width=10, command=self.update_task).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="Delete", width=10, command=self.delete_task).grid(row=0, column=2, padx=10)
        tk.Button(root, text="View Tasks", command=self.view_tasks).pack(pady=10)
        tk.Button(root, text="Clear All Tasks", command=self.clear_all, fg="red").pack(pady=10)

        # Load tasks from file
        self.load_tasks_from_file()

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append(task)
            self.refresh_listbox()
            self.task_entry.delete(0, tk.END)
            self.save_tasks_to_file()
            logger.info(f"Task added: {task}")
        else:
            messagebox.showwarning("Input Error", "Task field is empty!")

    def update_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            new_task = self.task_entry.get().strip()
            if new_task:
                index = selected_index[0]
                old_task = self.tasks[index]
                self.tasks[index] = new_task
                self.refresh_listbox()
                self.save_tasks_to_file()
                logger.info(f"Task updated from {old_task} to {new_task}")
            else:
                messagebox.showwarning("Input Error", "Task field is empty!")
        else:
            messagebox.showwarning("Selection Error", "Please select a task to update.")

    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:

            task = self.tasks.pop(selected_index[0])
            self.refresh_listbox()
            self.save_tasks_to_file()
            logger.info(f"Task deleted: {task}")
        else:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def view_tasks(self):
        if self.tasks:
            task_list_str = "\n".join(f"{i+1}. {task}" for i, task in enumerate(self.tasks))
            messagebox.showinfo("Your Tasks", task_list_str)
            logger.info("Tasks viewed.")
        else:
            messagebox.showinfo("No Tasks", "Your task list is empty.")

    def clear_all(self):
        if self.tasks:
            if messagebox.askyesno("Confirm", "Are you sure you want to delete all tasks?"):
                self.tasks.clear()
                self.refresh_listbox()
                self.save_tasks_to_file()
                logger.warning("All tasks cleared by user.")
        else:
            messagebox.showinfo("Info", "No tasks to clear.")

    def refresh_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)

    def save_tasks_to_file(self, filename="tasks.txt"):
        try:
            with open(filename, "w") as f:
                for task in self.tasks:
                    f.write(task + "\n")
            logger.info("Tasks saved to file.")
        except Exception as e:
            logger.error(f"Failed to save tasks: {e}")
            messagebox.showerror("Error", "Failed to save tasks.")

    def load_tasks_from_file(self, filename="tasks.txt"):
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    self.tasks = [line.strip() for line in f.readlines()]
                self.refresh_listbox()
                logger.info("Tasks loaded from file.")
            except Exception as e:
                logger.error(f"Failed to load tasks: {e}")
                messagebox.showerror("Error", "Failed to load tasks.")


if __name__ == "__main__":
    TaskManagerApp().run()
