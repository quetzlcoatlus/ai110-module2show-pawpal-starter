from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time, datetime, timedelta
from typing import List, Optional, Dict, Tuple


@dataclass
class Task:
    """Represents a single activity for a pet.

    Attributes:
        description: text description
        date: scheduled date
        scheduled_time: time of day
        frequency: e.g. 'once', 'daily', 'weekly'
        duration: optional duration of the activity
        completed: whether the task is done
    """
    description: str
    date: date
    scheduled_time: time
    frequency: str = "once"
    duration: Optional[timedelta] = None
    completed: bool = False

    def mark_complete(self) -> None:
        self.completed = True

    def reschedule(self, new_date: date, new_time: time) -> None:
        self.date = new_date
        self.scheduled_time = new_time

    def get_start_datetime(self) -> datetime:
        return datetime.combine(self.date, self.scheduled_time)

    def get_end_datetime(self) -> Optional[datetime]:
        if self.duration is None:
            return None
        end = self.get_start_datetime() + self.duration
        # handle cross-day if duration pushes into next day
        return end


@dataclass
class Pet:
    """Pet stores basic details and the tasks relevant to this pet."""
    name: str
    species: Optional[str] = None
    age: Optional[int] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        try:
            self.tasks.remove(task)
        except ValueError:
            pass

    def get_tasks(self) -> List[Task]:
        return list(self.tasks)


class Owner:
    """Owner manages multiple pets and exposes their tasks to the Scheduler."""

    def __init__(self, name: str, pets: Optional[List[Pet]] = None, preferences: Optional[Dict] = None):
        self.name = name
        self.pets: List[Pet] = pets if pets is not None else []
        self.preferences: Dict = preferences if preferences is not None else {}

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Gets tasks from all of the pets associated with owner"""
        tasks: List[Task] = []
        for p in self.pets:
            tasks.extend(p.get_tasks())
        return tasks


class Scheduler:
    """Scheduler is the brain that retrieves, organizes and manages tasks across pets/owners."""

    def __init__(self, owners: Optional[List[Owner]] = None):
        self.owners: List[Owner] = owners if owners is not None else []

    def add_owner(self, owner: Owner) -> None:
        self.owners.append(owner)

    def retrieve_tasks_for_date(self, date_: date) -> List[Task]:
        """Return all tasks for the given date across all owners/pets."""
        results: List[Task] = []
        for owner in self.owners:
            for t in owner.get_all_tasks():
                if t.date == date_:
                    results.append(t)
        return results

    def organize_tasks_for_date(self, date_: Optional[date] = None) -> List[Task]:
        """Return tasks for date sorted by time.

        If date_ is None, uses today's date.
        """
        target = date_ or date.today()
        tasks = self.retrieve_tasks_for_date(target)
        return sorted(tasks, key=lambda t: t.scheduled_time)

    def filter_tasks(self, *, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Return tasks filtered by completion status and/or pet name and optional date.

        Args:
            completed: if set, only return tasks whose `completed` matches this value.
            pet_name: if set, only return tasks for pets whose name matches (case-insensitive).

        The filter combines conditions (AND). If no filters provided, returns all tasks across owners.
        """
        results: List[Task] = []
        for owner in self.owners:
            for pet in owner.pets:
                if pet_name is not None and pet.name.lower() != pet_name.lower():
                    continue
                for t in pet.get_tasks():
                    if completed is not None and t.completed != completed:
                        continue
                    results.append(t)

        return results

    def detect_task_conflicts(self) -> List[Tuple[Pet, Task, Task]]:
        """Detect overlapping tasks per pet (simpler, faster).

        Strategy:
        - For each pet build (task, start, end) where end = start + duration if set,
          otherwise end = start + BUFFER (treat as a point with buffer).
        - Sort by start and scan forward, comparing only tasks whose start <= current end.
        - Print a warning for each detected conflict and return the list of conflicts.
        """
        conflicts: List[Tuple[Pet, Task, Task]] = []
        BUFFER = timedelta(minutes=15)

        for owner in self.owners:
            for pet in owner.pets:
                entries: List[Tuple[Task, datetime, datetime]] = []
                for t in pet.get_tasks():
                    try:
                        s = t.get_start_datetime()
                        e = t.get_end_datetime() if t.get_end_datetime() is not None else s + BUFFER
                        entries.append((t, s, e))
                    except Exception as exc:
                        print(f"Warning: failed to evaluate times for task '{t.description}' of pet '{pet.name}': {exc}")
                        continue

                entries.sort(key=lambda item: item[1])  # sort by start time

                n = len(entries)
                for i in range(n):
                    ti, si, ei = entries[i]
                    j = i + 1
                    # compare with subsequent tasks while their start is <= current end
                    while j < n and entries[j][1] <= ei:
                        tj, sj, ej = entries[j]
                        # if both have durations, require true overlap; otherwise buffer logic already applied
                        if (ti.duration is not None and tj.duration is not None and max(si, sj) < min(ei, ej)) or \
                           not (ti.duration is not None and tj.duration is not None):
                            conflicts.append((pet, ti, tj))
                            print(
                                f"Warning: conflict detected for pet '{pet.name}' - "
                                f"'{ti.description}' ({ti.date} {ti.scheduled_time}) "
                                f"conflicts with '{tj.description}' ({tj.date} {tj.scheduled_time})"
                            )
                        # extend current window to handle chains of overlapping tasks
                        ei = max(ei, ej)
                        j += 1

        return conflicts

    def assign_task_to_pet(self, task: Task, pet: Pet) -> None:
        pet.add_task(task)

    def _find_pet_for_task(self, task: Task) -> Optional[Pet]:
        """Return the Pet instance that currently holds `task`, or None."""
        for owner in self.owners:
            for pet in owner.pets:
                for t in pet.get_tasks():
                    if t is task:
                        return pet
        return None

    def mark_task_complete(self, task: Task) -> None:
        """Mark a task complete and, for recurring tasks, create the next occurrence.

        If a task has `frequency` of 'daily' or 'weekly', this will create and add
        a new Task scheduled at the same time on the next day/week.
        """
        if task.completed:
            return

        task.mark_complete()

        pet = self._find_pet_for_task(task)
        if pet is None:
            return

        freq = (task.frequency or '').lower()
        if freq == 'daily':
            delta = timedelta(days=1)
        elif freq == 'weekly':
            delta = timedelta(weeks=1)
        else:
            return

        next_date = task.date + delta
        new_task = Task(
            description=task.description,
            date=next_date,
            scheduled_time=task.scheduled_time,
            frequency=task.frequency,
            duration=task.duration,
            completed=False,
        )
        pet.add_task(new_task)
