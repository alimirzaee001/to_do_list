# ToDo List Application (Python OOP)

A comprehensive ToDo List application built with Python Object-Oriented Programming principles, featuring in-memory storage and a command-line interface.

## 🚀 Features

### Project Management
- ✅ Create projects with detailed descriptions (minimum 150 characters)
- ✅ List all projects with task counts
- ✅ Update project names and descriptions
- ✅ Delete projects (with cascade delete for associated tasks)
- ✅ Project name uniqueness validation
- ✅ Configurable maximum number of projects

### Task Management
- ✅ Create tasks within projects (minimum 150 characters description)
- ✅ Update task details (title, description, deadline)
- ✅ Change task status (todo → doing → done)
- ✅ Delete individual tasks
- ✅ Set optional task deadlines with validation
- ✅ Configurable maximum tasks per project

### Data Validation & Constraints
- ✅ Minimum length requirements for names and descriptions
- ✅ Date validation for deadlines (cannot be in the past)
- ✅ Status validation (only todo/doing/done allowed)
- ✅ Project name uniqueness
- ✅ Configurable limits via environment variables

### User Interface
- ✅ Intuitive command-line interface with emoji indicators
- ✅ Clear error messages and success confirmations
- ✅ Interactive project and task selection
- ✅ Confirmation prompts for destructive operations

## 📋 Requirements

- Python 3.8 or higher
- Poetry (for dependency management)

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd todo-list-oop
   ```

2. **Install dependencies using Poetry:**
   ```bash
   poetry install
   ```

3. **Configure environment (optional):**
   ```bash
   cp .env.example .env
   # Edit .env to customize MAX_NUMBER_OF_PROJECTS and MAX_NUMBER_OF_TASKS
   ```

## 🎯 Usage

### Running the Application

```bash
# Using Poetry
poetry run todo-cli

# Or activate the virtual environment and run directly
poetry shell
todo-cli
```

### Application Menu

The application provides a simple menu-driven interface:

1. **Create Project** - Create a new project with name and description
2. **List Projects** - View all projects with their details
3. **Update Project** - Modify project name and/or description
4. **Delete Project** - Remove a project and all its tasks
5. **Create Task** - Add a new task to an existing project
6. **List Project Tasks** - View all tasks in a specific project
7. **Update Task** - Modify task details
8. **Update Task Status** - Change task status (todo/doing/done)
9. **Delete Task** - Remove a specific task
0. **Exit** - Close the application

## ⚙️ Configuration

The application uses environment variables for configuration:

```env
# Maximum number of projects a user can create
MAX_NUMBER_OF_PROJECTS=10

# Maximum number of tasks per project
MAX_NUMBER_OF_TASKS=100
```

## 🏗️ Architecture

### Project Structure
```
todo-list-oop/
├── todo_list/
│   ├── __init__.py          # Package initialization
│   ├── models.py            # Core data models (Project, Task)
│   ├── config.py            # Configuration management
│   ├── storage.py           # In-memory storage layer
│   └── cli.py              # Command-line interface
├── pyproject.toml          # Poetry configuration
├── .env                    # Environment variables
├── .env.example           # Example configuration
└── README.md              # This file
```

### Design Patterns Used

- **Data Classes**: For clean data structure definitions
- **Repository Pattern**: Storage layer abstraction
- **Configuration Management**: Environment-based settings
- **Input Validation**: Comprehensive validation with clear error messages
- **Cascade Delete**: Automatic cleanup of related data

### OOP Principles

- **Encapsulation**: Clear boundaries between layers
- **Single Responsibility**: Each class has a specific purpose
- **Type Hints**: Comprehensive type annotations
- **Error Handling**: Proper exception handling and user feedback

## 🔄 Development Workflow

### Git Strategy

- **main**: Production-ready code only
- **develop**: Main development branch
- **feature/***: Feature-specific branches

### Commit Guidelines

All commits must follow conventional commit format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation updates
- `refactor:` for code improvements
- `test:` for test additions

## 🧪 Testing

```bash
# Run tests (when implemented)
poetry run pytest

# Run with coverage
poetry run pytest --cov=todo_list

# Run linting
poetry run flake8 todo_list/
poetry run black todo_list/
```

## 🚧 Future Enhancements

This is Phase 1 of the project. Future phases will include:

- **Phase 2**: Persistent storage (JSON/SQLite)
- **Phase 3**: Web API with FastAPI
- **Phase 4**: Automated testing
- **Phase 5**: Web frontend

## 📚 Learning Objectives

This project demonstrates:

- Python OOP best practices
- Clean architecture principles
- Configuration management
- Input validation and error handling
- CLI application development
- Project structure and organization
- Git workflow and version control

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is for educational purposes as part of a Software Engineering course.

## 🆘 Support

For issues or questions:
1. Check existing documentation
2. Review the code comments
3. Create an issue in the repository

---

**Note**: This application uses in-memory storage, so all data will be lost when the application exits. This is intentional for Phase 1 to focus on OOP principles and architecture.
