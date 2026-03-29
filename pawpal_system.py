from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import List, Optional


@dataclass
class Task:
    """Represents a pet care task."""
    description: str
    time: str
    date: date
    frequency: str = "once"
    completed: bool = False
    pet_name: str = ""

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def is_recurring(self) -> bool:
        """Return whether the task is recurring."""
        return self.frequency.lower() in {"daily", "weekly"}

    def next_occurrence(self) -> Optional["Task"]:
        """Create the next recurring task instance."""
        if self.frequency.lower() == "daily":
            next_date = self.date + timedelta(days=1)
        elif self.frequency.lower() == "weekly":
            next_date = self.date + timedelta(weeks=1)
        else:
            return None

        return Task(
            description=self.description,
            time=self.time,
            date=next_date,
            frequency=self.frequency,
            completed=False,
            pet_name=self.pet_name,
        )


@dataclass
class Pet:
    """Represents a pet and its tasks."""
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the pet."""
        task.pet_name = self.name
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks for the pet."""
        return self.tasks

    def get_incomplete_tasks(self) -> List[Task]:
        """Return incomplete tasks for the pet."""
        return [task for task in self.tasks if not task.completed]

    def get_tasks_by_status(self, completed: bool) -> List[Task]:
        """Filter tasks by completion status."""
        return [task for task in self.tasks if task.completed == completed]


@dataclass
class Owner:
    """Represents a pet owner with multiple pets."""
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner."""
        self.pets.append(pet)

    def get_pet(self, name: str) -> Optional[Pet]:
        """Find a pet by name."""
        for pet in self.pets:
            if pet.name.lower() == name.lower():
                return pet
        return None

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """Handles sorting, filtering, recurrence, and conflict checks."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def get_schedule_for_day(self, day: date) -> List[Task]:
        """Return tasks for a specific day."""
        return [task for task in self.owner.get_all_tasks() if task.date == day]

    def get_todays_tasks(self) -> List[Task]:
        """Return tasks for today."""
        return self.get_schedule_for_day(date.today())

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted by time."""
        return sorted(tasks, key=lambda task: datetime.strptime(task.time, "%H:%M"))

    def filter_tasks(
        self,
        tasks: List[Task],
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None
    ) -> List[Task]:
        """Filter tasks by pet name and completion status."""
        filtered = tasks

        if pet_name is not None:
            filtered = [task for task in filtered if task.pet_name.lower() == pet_name.lower()]

        if completed is not None:
            filtered = [task for task in filtered if task.completed == completed]

        return filtered

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Return warnings when tasks share the same date and time."""
        warnings = []
        seen = {}

        for task in tasks:
            key = (task.date, task.time)
            if key in seen:
                other = seen[key]
                warnings.append(
                    f"Conflict: '{other.description}' for {other.pet_name} and "
                    f"'{task.description}' for {task.pet_name} are both at {task.time} "
                    f"on {task.date}."
                )
            else:
                seen[key] = task

        return warnings

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Mark task complete and create a new occurrence if recurring."""
        task.mark_complete()
        new_task = task.next_occurrence()

        if new_task:
            pet = self.owner.get_pet(task.pet_name)
            if pet:
                pet.add_task(new_task)

        return new_task