import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import messagebox


DATA_FILE = Path(__file__).with_name("tasks.json")
DATE_FORMAT = "%Y-%m-%d"


@dataclass
class Task:
    title: str
    due_date: str
    priority: str
    done: bool = False


class TodoApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Your Task Manager (❁´◡`❁)")
        self.root.geometry("620x560")
        self.root.minsize(620, 560)
        self.root.configure(bg="#f5efe6")

        self.tasks: list[Task] = []

        self._build_ui()
        self._load_tasks()
        self._refresh_list()

    def _build_ui(self) -> None:
        self._style = {
            "bg": "#fefefe",
            "panel": "#EFE5EB",
            "accent": "#c78cbe",
            "text": "#2f2f2f",
            "muted": "#6a6a6a",
            "done": "#8a8a8a",
            "line": "#ece4d9",
        }

        main = tk.Frame(self.root, bg=self._style["bg"], padx=(72, 18), pady=18)
        main.pack(fill="both", expand=True)

        header = tk.Frame(main, bg=self._style["bg"])
        header.pack(fill="x")

        tk.Label(
            header,
            text="Time⏱️+ Task Planner📝",
            bg=self._style["bg"],
            fg=self._style["text"],
            font=("Segoe UI Semibold", 24),
        ).pack(anchor="w")
        tk.Label(
            header,
            text="Plan your day 👌",
            bg=self._style["bg"],
            fg=self._style["muted"],
            font=("Segoe UI", 11),
        ).pack(anchor="w", pady=(2, 12))

        content = tk.Frame(main, bg=self._style["bg"])
        content.pack(fill="both", expand=True)

        form = tk.Frame(content, bg=self._style["panel"], padx=12, pady=12, bd=0)
        form.pack(fill="x", pady=(0, 12))

        tk.Label(form, text="Task", bg=self._style["panel"], fg=self._style["text"]).grid(row=0, column=0, sticky="w")
        self.task_entry = tk.Entry(form, font=("Segoe UI", 11), width=30, relief="flat", bg="#fafafa")
        self.task_entry.grid(row=1, column=0, padx=(0, 12), pady=(4, 10), sticky="ew")

        tk.Label(form, text="Due Date (YYYY-MM-DD)", bg=self._style["panel"], fg=self._style["text"]).grid(row=0, column=1, sticky="w")
        self.date_entry = tk.Entry(form, font=("Segoe UI", 11), width=12, relief="flat", bg="#fafafa")
        self.date_entry.grid(row=1, column=1, padx=(0, 12), pady=(4, 10), sticky="ew")

        tk.Label(form, text="Priority", bg=self._style["panel"], fg=self._style["text"]).grid(row=0, column=2, sticky="w")
        self.priority_var = tk.StringVar(value="Medium")
        self.priority_menu = tk.OptionMenu(form, self.priority_var, "Low", "Medium", "High")
        self.priority_menu.config(font=("Segoe UI", 10), relief="flat", bg="#fafafa", highlightthickness=0)
        self.priority_menu.grid(row=1, column=2, pady=(4, 10), sticky="ew")

        add_btn = tk.Button(
            form,
            text="Add Task",
            command=self.add_task,
            font=("Segoe UI Semibold", 10),
            bg=self._style["accent"],
            fg="white",
            activebackground="#e07a4f",
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
        )
        add_btn.grid(row=1, column=3, sticky="ew")

        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=0)
        form.columnconfigure(2, weight=0)
        form.columnconfigure(3, weight=0)

        list_panel = tk.Frame(content, bg=self._style["panel"], padx=12, pady=12)
        list_panel.pack(fill="both", expand=True)

        tk.Label(
            list_panel,
            text="Tasks",
            bg=self._style["panel"],
            fg=self._style["text"],
            font=("Segoe UI Semibold", 13),
        ).pack(anchor="w")

        self.listbox = tk.Listbox(
            list_panel,
            font=("Segoe UI", 11),
            bg="#fffdfe",
            fg=self._style["text"],
            selectbackground="#ffc7e5",
            activestyle="none",
            bd=0,
            highlightthickness=1,
            highlightbackground=self._style["line"],
        )
        self.listbox.pack(fill="both", expand=True, pady=(8, 10))

        actions = tk.Frame(list_panel, bg=self._style["panel"])
        actions.pack(fill="x")

        self._action_button(actions, "Mark Done / Undo", self.toggle_done).pack(side="left", pads=(0, 8))
        self._action_button(actions, "Delete Task", self.delete_task).pack(side="left", padx=(0, 8))
        self._action_button(actions, "Clear Completed", self.clear_completed).pack(side="left")

    def _action_button(self, parent: tk.Widget, text: str, command) -> tk.Button:
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10),
            bg="#f0f0f0",
            fg=self._style["text"],
            activebackground="#e7e7e7",
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
        )

    def _priority_rank(self, priority: str) -> int:
        return {"High": 0, "Medium": 1, "Low": 2}.get(priority, 3)

    def _due_rank(self, due_date: str) -> datetime:
        try:
            return datetime.strptime(due_date, DATE_FORMAT)
        except ValueError:
            return datetime.max

    def _refresh_list(self) -> None:
        self.tasks.sort(key=lambda t: (t.done, self._priority_rank(t.priority), self._due_rank(t.due_date), t.title.lower()))
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "DONE" if task.done else "TODO"
            line = f"[{status}] {task.title} | Due: {task.due_date} | Priority: {task.priority}"
            self.listbox.insert(tk.END, line)
            if task.done:
                self.listbox.itemconfig(tk.END, fg=self._style["done"])

    def _save_tasks(self) -> None:
        DATA_FILE.write_text(json.dumps([asdict(t) for t in self.tasks], indent=2), encoding="utf-8")

    def _load_tasks(self) -> None:
        if not DATA_FILE.exists():
            return
        try:
            raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            self.tasks = [Task(**item) for item in raw if isinstance(item, dict)]
        except (json.JSONDecodeError, TypeError):
            messagebox.showwarning("Data Warning", "Could not read tasks.json, starting with an empty list.")
            self.tasks = []

    def add_task(self) -> None:
        title = self.task_entry.get().strip()
        due_date = self.date_entry.get().strip() or "No date"
        priority = self.priority_var.get()

        if not title:
            messagebox.showinfo("Missing Task", "Please enter a task name.")
            return

        if due_date != "No date":
            try:
                datetime.strptime(due_date, DATE_FORMAT)
            except ValueError:
                messagebox.showerror("Date Format", "Use date format YYYY-MM-DD.")
                return

        self.tasks.append(Task(title=title, due_date=due_date, priority=priority))
        self._save_tasks()
        self._refresh_list()

        self.task_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.priority_var.set("Medium")
        self.task_entry.focus_set()

    def _selected_index(self) -> int | None:
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showinfo("No Selection", "Select a task first.")
            return None
        return int(selected[0])

    def toggle_done(self) -> None:
        idx = self._selected_index()
        if idx is None:
            return
        self.tasks[idx].done = not self.tasks[idx].done
        self._save_tasks()
        self._refresh_list()

    def delete_task(self) -> None:
        idx = self._selected_index()
        if idx is None:
            return
        del self.tasks[idx]
        self._save_tasks()
        self._refresh_list()

    def clear_completed(self) -> None:
        self.tasks = [t for t in self.tasks if not t.done]
        self._save_tasks()
        self._refresh_list()


def main() -> None:
    root = tk.Tk()
    app = TodoApp(root)
    app.task_entry.focus_set()
    root.mainloop()


if __name__ == "__main__":
    main()
