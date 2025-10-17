"""
Command Line Interface for the ToDo List application.

This module provides a user-friendly CLI for managing projects and tasks.
"""

import sys
from typing import Optional
from datetime import datetime
from .storage import storage
from .models import TaskStatus


class TodoCLI:
    """Command Line Interface for the ToDo List application."""

    def __init__(self):
        """Initialize the CLI."""
        self.storage = storage

    def show_menu(self) -> None:
        """Display the main menu."""
        print("\n" + "="*50)
        print("📋 ToDo List Application")
        print("="*50)
        print("1. Create Project")
        print("2. List Projects")
        print("3. Update Project")
        print("4. Delete Project")
        print("5. Create Task")
        print("6. List Project Tasks")
        print("7. Update Task")
        print("8. Update Task Status")
        print("9. Delete Task")
        print("0. Exit")
        print("="*50)

    def get_user_choice(self) -> str:
        """Get user's menu choice."""
        while True:
            try:
                choice = input("Enter your choice (0-9): ").strip()
                if choice in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    return choice
                else:
                    print("❌ Invalid choice. Please enter a number between 0-9.")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                sys.exit(0)

    def create_project(self) -> None:
        """Create a new project."""
        print("\n📁 Create New Project")
        print("-" * 30)

        name = input("Enter project name (min 30 characters): ").strip()
        if not name:
            print("❌ Project name cannot be empty.")
            return

        description = input("Enter project description (min 150 characters): ").strip()
        if not description:
            print("❌ Project description cannot be empty.")
            return

        try:
            project = self.storage.create_project(name, description)
            print(f"✅ Project created successfully!")
            print(f"   ID: {project.project_id}")
            print(f"   Name: {project.name}")
            print(f"   Created: {project.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        except ValueError as e:
            print(f"❌ Error: {e}")

    def list_projects(self) -> None:
        """List all projects."""
        print("\n📂 All Projects")
        print("-" * 30)

        projects = self.storage.list_projects()

        if not projects:
            print("📭 No projects found. Create your first project!")
            return

        for i, project in enumerate(projects, 1):
            task_count = len([t for t in self.storage.tasks.values()
                            if t.project_id == project.project_id])
            print(f"{i}. [{project.project_id}]")
            print(f"   Name: {project.name}")
            print(f"   Description: {project.description[:100]}{'...' if len(project.description) > 100 else ''}")
            print(f"   Tasks: {task_count}")
            print(f"   Created: {project.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print()

    def update_project(self) -> None:
        """Update an existing project."""
        print("\n✏️  Update Project")
        print("-" * 30)

        project_id = input("Enter project ID: ").strip()
        if not project_id:
            print("❌ Project ID cannot be empty.")
            return

        project = self.storage.get_project(project_id)
        if not project:
            print(f"❌ Project with ID '{project_id}' not found.")
            return

        print(f"Current name: {project.name}")
        print(f"Current description: {project.description[:100]}{'...' if len(project.description) > 100 else ''}")

        name = input("Enter new name (leave empty to keep current): ").strip()
        description = input("Enter new description (leave empty to keep current): ").strip()

        try:
            updated_project = self.storage.update_project(
                project_id,
                name=name if name else None,
                description=description if description else None
            )
            print("✅ Project updated successfully!")
        except ValueError as e:
            print(f"❌ Error: {e}")

    def delete_project(self) -> None:
        """Delete a project."""
        print("\n🗑️  Delete Project")
        print("-" * 30)

        project_id = input("Enter project ID: ").strip()
        if not project_id:
            print("❌ Project ID cannot be empty.")
            return

        project = self.storage.get_project(project_id)
        if not project:
            print(f"❌ Project with ID '{project_id}' not found.")
            return

        confirm = input(f"Are you sure you want to delete project '{project.name}'? (yes/no): ").strip().lower()
        if confirm not in ['yes', 'y']:
            print("❌ Operation cancelled.")
            return

        try:
            success = self.storage.delete_project(project_id)
            if success:
                print("✅ Project deleted successfully!")
            else:
                print("❌ Failed to delete project.")
        except Exception as e:
            print(f"❌ Error: {e}")

    def create_task(self) -> None:
        """Create a new task."""
        print("\n✅ Create New Task")
        print("-" * 30)

        # List available projects
        projects = self.storage.list_projects()
        if not projects:
            print("❌ No projects available. Create a project first!")
            return

        print("Available projects:")
        for i, project in enumerate(projects, 1):
            print(f"{i}. {project.name}")

        try:
            project_choice = int(input("Select project (number): ")) - 1
            if project_choice < 0 or project_choice >= len(projects):
                print("❌ Invalid project selection.")
                return
        except ValueError:
            print("❌ Please enter a valid number.")
            return

        project_id = projects[project_choice].project_id

        title = input("Enter task title (min 30 characters): ").strip()
        if not title:
            print("❌ Task title cannot be empty.")
            return

        description = input("Enter task description (min 150 characters): ").strip()
        if not description:
            print("❌ Task description cannot be empty.")
            return

        deadline_input = input("Enter deadline (YYYY-MM-DD, leave empty for none): ").strip()

        try:
            task = self.storage.create_task(
                project_id=project_id,
                title=title,
                description=description,
                deadline=deadline_input if deadline_input else None
            )
            print("✅ Task created successfully!")
            print(f"   ID: {task.task_id}")
            print(f"   Status: {task.status.value}")
            if task.deadline:
                print(f"   Deadline: {task.deadline}")
        except ValueError as e:
            print(f"❌ Error: {e}")

    def list_project_tasks(self) -> None:
        """List all tasks in a project."""
        print("\n📋 Project Tasks")
        print("-" * 30)

        projects = self.storage.list_projects()
        if not projects:
            print("❌ No projects available.")
            return

        print("Available projects:")
        for i, project in enumerate(projects, 1):
            print(f"{i}. {project.name}")

        try:
            project_choice = int(input("Select project (number): ")) - 1
            if project_choice < 0 or project_choice >= len(projects):
                print("❌ Invalid project selection.")
                return
        except ValueError:
            print("❌ Please enter a valid number.")
            return

        project_id = projects[project_choice].project_id
        tasks = self.storage.get_project_tasks(project_id)

        if not tasks:
            print(f"📭 No tasks found in project '{projects[project_choice].name}'.")
            return

        print(f"\nTasks in '{projects[project_choice].name}':")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. [{task.task_id}] {task.title}")
            print(f"   Status: {task.status.value}")
            print(f"   Description: {task.description[:100]}{'...' if len(task.description) > 100 else ''}")
            if task.deadline:
                print(f"   Deadline: {task.deadline}")
            print(f"   Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print()

    def update_task(self) -> None:
        """Update an existing task."""
        print("\n✏️  Update Task")
        print("-" * 30)

        task_id = input("Enter task ID: ").strip()
        if not task_id:
            print("❌ Task ID cannot be empty.")
            return

        task = self.storage.get_task(task_id)
        if not task:
            print(f"❌ Task with ID '{task_id}' not found.")
            return

        print(f"Current title: {task.title}")
        print(f"Current description: {task.description[:100]}{'...' if len(task.description) > 100 else ''}")
        if task.deadline:
            print(f"Current deadline: {task.deadline}")
        print(f"Current status: {task.status.value}")

        title = input("Enter new title (leave empty to keep current): ").strip()
        description = input("Enter new description (leave empty to keep current): ").strip()
        deadline = input("Enter new deadline (YYYY-MM-DD, leave empty to keep current): ").strip()

        try:
            updated_task = self.storage.update_task(
                task_id=task_id,
                title=title if title else None,
                description=description if description else None,
                deadline=deadline if deadline else None
            )
            print("✅ Task updated successfully!")
        except ValueError as e:
            print(f"❌ Error: {e}")

    def update_task_status(self) -> None:
        """Update task status."""
        print("\n🔄 Update Task Status")
        print("-" * 30)

        task_id = input("Enter task ID: ").strip()
        if not task_id:
            print("❌ Task ID cannot be empty.")
            return

        task = self.storage.get_task(task_id)
        if not task:
            print(f"❌ Task with ID '{task_id}' not found.")
            return

        print(f"Current status: {task.status.value}")
        print("Available statuses:")
        print("1. todo")
        print("2. doing")
        print("3. done")

        try:
            choice = input("Select new status (1-3): ").strip()
            status_map = {'1': TaskStatus.TODO, '2': TaskStatus.DOING, '3': TaskStatus.DONE}

            if choice not in status_map:
                print("❌ Invalid status selection.")
                return

            new_status = status_map[choice]
            task.update_status(new_status)
            print(f"✅ Task status updated to: {new_status.value}")

        except Exception as e:
            print(f"❌ Error: {e}")

    def delete_task(self) -> None:
        """Delete a task."""
        print("\n🗑️  Delete Task")
        print("-" * 30)

        task_id = input("Enter task ID: ").strip()
        if not task_id:
            print("❌ Task ID cannot be empty.")
            return

        task = self.storage.get_task(task_id)
        if not task:
            print(f"❌ Task with ID '{task_id}' not found.")
            return

        confirm = input(f"Are you sure you want to delete task '{task.title}'? (yes/no): ").strip().lower()
        if confirm not in ['yes', 'y']:
            print("❌ Operation cancelled.")
            return

        try:
            success = self.storage.delete_task(task_id)
            if success:
                print("✅ Task deleted successfully!")
            else:
                print("❌ Failed to delete task.")
        except Exception as e:
            print(f"❌ Error: {e}")

    def run(self) -> None:
        """Run the CLI application."""
        print("🚀 Welcome to ToDo List Application!")

        while True:
            try:
                self.show_menu()
                choice = self.get_user_choice()

                if choice == '0':
                    print("👋 Goodbye!")
                    break
                elif choice == '1':
                    self.create_project()
                elif choice == '2':
                    self.list_projects()
                elif choice == '3':
                    self.update_project()
                elif choice == '4':
                    self.delete_project()
                elif choice == '5':
                    self.create_task()
                elif choice == '6':
                    self.list_project_tasks()
                elif choice == '7':
                    self.update_task()
                elif choice == '8':
                    self.update_task_status()
                elif choice == '9':
                    self.delete_task()

                input("\nPress Enter to continue...")

            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                input("Press Enter to continue...")


def main():
    """Main entry point for the CLI application."""
    try:
        cli = TodoCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
