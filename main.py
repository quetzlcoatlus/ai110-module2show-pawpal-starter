"""
Testing ground for pawpal_system.py
"""

from pawpal_system import Task, Pet, Owner, Scheduler
from datetime import date, time, timedelta

test_task1 = Task("Walk", date(2026,3,23), time(12), duration=timedelta(hours=1))
test_task2 = Task("Meds", date(2026,3,23), time(), "monthly")
test_task3 = Task("Bath", date(2026,3,23), time(10), duration=timedelta(hours=1))

test_conflict_task1 = Task("Walk", date(2026,3,23), time(12), duration=timedelta(hours=1))

test_pet1 = Pet("Sparky", tasks=[test_task1, test_task3, test_conflict_task1])
test_pet2 = Pet("Charlie", tasks=[test_task2])

test_owner = Owner("Test", pets=[test_pet1, test_pet2])

test_scheduler = Scheduler(owners=[test_owner])

filtered = test_scheduler.filter_tasks(pet_name="Sparky")
sorted_tasks = test_scheduler.organize_tasks_for_date(date(2026,3,23))
conflicts = test_scheduler.detect_task_conflicts()

print("Today's Schedule")
for task in sorted_tasks:
    print(f"  - {task.description} at {task.scheduled_time} (Duration: {task.duration})")

# Need to implement logic for sorting tasks by time, 
# filtering by pet/status, 
# handling recurring tasks, 
# and conflict detection