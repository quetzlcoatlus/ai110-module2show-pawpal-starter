from datetime import date, time, timedelta

from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete_changes_status():
	"""Verify that calling mark_complete() actually changes task's status."""
	t = Task(description="Feed", date=date.today(), scheduled_time=time(9, 0))
	assert not t.completed
	t.mark_complete()
	assert t.completed


def test_adding_task_increases_pet_task_count():
	"""Verify adding task to Pet increases pet's task count."""
	p = Pet(name="Fido")
	assert len(p.get_tasks()) == 0
	t = Task(description="Walk", date=date.today(), scheduled_time=time(18, 30))
	p.add_task(t)
	assert len(p.get_tasks()) == 1


def test_tasks_sorted_chronologically():
	"""Verify tasks are returned in chronological order by date and time."""
	o = Owner("John")
	p = Pet(name="Fido")
	today = date.today()
	t1 = Task(description="Feed", date=today, scheduled_time=time(9, 0))
	t2 = Task(description="Walk", date=today, scheduled_time=time(18, 30))
	t3 = Task(description="Groom", date=today, scheduled_time=time(10, 0))
	s = Scheduler()
	s.add_owner(o)
	s.add_pet_to_owner(p, o)
	s.assign_task_to_pet(t1, p)
	s.assign_task_to_pet(t2, p)
	s.assign_task_to_pet(t3, p)
	tasks = s.organize_tasks_for_date()
	assert tasks[0].description == "Feed"
	assert tasks[1].description == "Groom"
	assert tasks[2].description == "Walk"


def test_daily_task_recurrence():
	"""Verify marking a daily task complete creates a new task for the next day."""
	o = Owner("John")
	p = Pet(name="Fido")
	t = Task(description="Feed", date=date.today(), scheduled_time=time(9, 0), frequency="daily")
	s = Scheduler()
	s.add_owner(o)
	s.add_pet_to_owner(p, o)
	s.assign_task_to_pet(t, p)
	
	assert not t.completed
	s.mark_task_complete(t)
	assert t.completed

	# Assuming Pet or system handles recurrence; check if new task is created
	next_day = date.today() + timedelta(days=1)
	assert s.organize_tasks_for_date(next_day)


def test_conflict_detection():
	"""Verify scheduler flags duplicate times for the same pet."""
	s = Scheduler()
	o = Owner("John")
	p = Pet(name="Fido")
	t1 = Task(description="Feed", date=date.today(), scheduled_time=time(9, 0))
	t2 = Task(description="Walk", date=date.today(), scheduled_time=time(9, 0))  # Same time
	s.add_owner(o)
	s.add_pet_to_owner(p, o)
	s.assign_task_to_pet(t1, p)
	s.assign_task_to_pet(t2, p)

	conflicts = s.detect_task_conflicts()
	assert conflicts
