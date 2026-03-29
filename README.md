# PawPal+

PawPal+ is a smart pet care management system built with Python and Streamlit. It helps pet owners organize feeding, walks, medications, and appointments using object-oriented design and scheduling logic.

## Features
- Add and manage multiple pets
- Add tasks for each pet
- View today's tasks
- Sort tasks by time
- Detect schedule conflicts
- Automatically reschedule recurring daily and weekly tasks
- Mark tasks as complete through the UI

## Project Files
- `pawpal_system.py` - backend logic layer
- `main.py` - CLI demo script
- `app.py` - Streamlit user interface
- `tests/test_pawpal.py` - automated tests
- `reflection.md` - project reflection
- `requirements.txt` - project dependencies

## UML
```mermaid
classDiagram
    class Task {
        +description: str
        +time: str
        +date: date
        +frequency: str
        +completed: bool
        +pet_name: str
        +mark_complete()
        +is_recurring()
        +next_occurrence()
    }

    class Pet {
        +name: str
        +species: str
        +age: int
        +tasks: list
        +add_task(task)
        +get_tasks()
        +get_incomplete_tasks()
        +get_tasks_by_status(completed)
    }

    class Owner {
        +name: str
        +pets: list
        +add_pet(pet)
        +get_pet(name)
        +get_all_tasks()
    }

    class Scheduler {
        +owner: Owner
        +get_schedule_for_day(day)
        +get_todays_tasks()
        +sort_by_time(tasks)
        +filter_tasks(tasks, pet_name, completed)
        +detect_conflicts(tasks)
        +mark_task_complete(task)
    }

    Owner --> Pet
    Pet --> Task
    Scheduler --> Owner
```

## Running the CLI Demo
```bash
python3 main.py
```

## Running the Streamlit App
```bash
streamlit run app.py
```

## Testing PawPal+
```bash
python3 -m pytest
```

Tests cover:
- Task completion
- Task addition
- Sorting by time
- Recurring task creation
- Conflict detection

## Smarter Scheduling
PawPal+ supports:
- sorting tasks chronologically,
- identifying time conflicts,
- filtering tasks by pet or completion state,
- automatically creating the next task instance for recurring daily or weekly care items.

## Reflection
See `reflection.md` for design decisions, tradeoffs, and AI collaboration notes.

## Confidence Level
⭐⭐⭐⭐☆