from datetime import date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


def test_mark_complete_changes_status():
    task = Task("Feed", "09:00", date.today())
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Buddy", "Dog", 3)
    pet.add_task(Task("Walk", "08:00", date.today()))
    assert len(pet.tasks) == 1


def test_sort_by_time_returns_chronological_order():
    owner = Owner("Alex")
    pet = Pet("Buddy", "Dog", 3)
    owner.add_pet(pet)

    pet.add_task(Task("Late Task", "12:00", date.today()))
    pet.add_task(Task("Early Task", "08:00", date.today()))
    pet.add_task(Task("Mid Task", "10:30", date.today()))

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time(pet.tasks)

    assert [task.time for task in sorted_tasks] == ["08:00", "10:30", "12:00"]


def test_daily_recurrence_creates_next_day_task():
    owner = Owner("Alex")
    pet = Pet("Buddy", "Dog", 3)
    owner.add_pet(pet)

    today = date.today()
    task = Task("Walk", "08:00", today, "daily")
    pet.add_task(task)

    scheduler = Scheduler(owner)
    new_task = scheduler.mark_task_complete(task)

    assert task.completed is True
    assert new_task is not None
    assert new_task.date == today + timedelta(days=1)
    assert new_task.completed is False
    assert len(pet.tasks) == 2


def test_conflict_detection_flags_same_time_tasks():
    owner = Owner("Alex")
    dog = Pet("Buddy", "Dog", 3)
    cat = Pet("Milo", "Cat", 2)
    owner.add_pet(dog)
    owner.add_pet(cat)

    today = date.today()
    dog.add_task(Task("Walk", "08:00", today))
    cat.add_task(Task("Medication", "08:00", today))

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts(owner.get_all_tasks())

    assert len(conflicts) == 1
    assert "Conflict:" in conflicts[0]