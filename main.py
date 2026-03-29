from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler


def print_schedule(title, tasks):
    print(f"\n{title}")
    print("-" * len(title))
    if not tasks:
        print("No tasks scheduled.")
        return

    for task in tasks:
        status = "Done" if task.completed else "Pending"
        print(
            f"{task.time} | {task.pet_name:<10} | {task.description:<18} | "
            f"{task.frequency:<6} | {status}"
        )


def main():
    owner = Owner("Alex")

    buddy = Pet("Buddy", "Dog", 4)
    milo = Pet("Milo", "Cat", 2)

    owner.add_pet(buddy)
    owner.add_pet(milo)

    today = date.today()

    buddy.add_task(Task("Feed Breakfast", "07:30", today, "daily"))
    buddy.add_task(Task("Morning Walk", "08:00", today, "daily"))
    milo.add_task(Task("Medication", "08:00", today, "weekly"))
    milo.add_task(Task("Vet Visit", "15:00", today, "once"))

    scheduler = Scheduler(owner)

    tasks_today = scheduler.get_todays_tasks()
    sorted_tasks = scheduler.sort_by_time(tasks_today)
    print_schedule("Today's Schedule", sorted_tasks)

    conflicts = scheduler.detect_conflicts(sorted_tasks)
    if conflicts:
        print("\nConflict Warnings")
        print("-----------------")
        for warning in conflicts:
            print(warning)

    buddy_pending = scheduler.filter_tasks(sorted_tasks, pet_name="Buddy", completed=False)
    print_schedule("Buddy Pending Tasks", buddy_pending)

    recurring = buddy.tasks[1]
    scheduler.mark_task_complete(recurring)

    print("\nBuddy Tasks After Completing a Daily Task")
    print("-----------------------------------------")
    for task in buddy.tasks:
        status = "Done" if task.completed else "Pending"
        print(f"{task.date} | {task.time} | {task.description} | {task.frequency} | {status}")


if __name__ == "__main__":
    main()