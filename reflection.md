# PawPal+ Project Reflection

## 1. System Design

### Actions to program

Three core actions:
- Add a pet
- Schedule a walk (task with date, time duration, and priority)
- See today's tasks

Extended
- Schedule medication (task with date, priority and without time duration)
- Explain what constraints informed today's tasks
- Edit tasks

### Object building blocks

#### Pet
Attributes
- name: str

#### Owner
Attributes
- name: str
- pets: list<Pet>
- preferences: dict (e.g. preference: value)

Methods
- add_pet(Pet) -> adds pet to pets

#### Task
Attributes
- name: str
- priority: str category
- start_time (optional): time 
- end_time (optional): time
- date: date
- assigned_pets: list<Pet>

Methods
- init(name, priority, date, start_time = None, end_time = None)
- get_duration() -> difference between start and end times

#### Scheduler
Attributes
- tasks: list<Task>
- date: date (now)

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

UML diagram under ./UML, contains initial classes with their relationships, methods, and attributes.

Initial design included classes:
- pet: holds pet information and is assigned to task and owner
- owner: holds owner preferences and is associated with a set of pets
- task: holds task information and which pets they're related to. can be edited and can be aggregated in a schedule
- scheduler: holds a set of tasks for a given day to be displayed in the frontend

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Based on the README suggestions, I realized that it was asking for a Scheduler class so I changed that.

I also changed some relationships based on the README information. A pet has a list of tasks instead of a pet being assigned to a task. The owner provides access to their pets' tasks. The Scheduler is more broad and does CRUD on tasks across pets.

Regenerated the mermaid diagram and regenerated the structure for the pawpal_system.py file.

For each class, specific changes:

**Task**

Attributes
-name
+description: str
-end_time
-start_time
+scheduled_time: time
+frequency: str (once, weekly, daily, etc)
+completed: bool
+Optional(duration): timedelta

Methods
+mark_complete()
+reschedule(new_time)

**Pet**
Has tasks

Attributes
+species: str
+age: int
+tasks: list<Task>

Methods
+add_task(task) -> None
+remove_task(task) -> None
+get_tasks() -> list

**Owner**
Has pets

Methods
+get_all_tasks() -> list of tasks from owner's pets

**Scheduler**
Manages owners

Attributes
+owners: list<Owner>

Methods
+retrieve_tasks(date) -> list of all tasks for date across owners/pets
+organize_tasks(Optional(date)) -> sorted list of tasks chronologically across date or today's date
+detect_conflicts() -> list of all conflicts for tasks across all owners/pets
+assign_task_to_pet(task, pet) -> None

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

Scheduler considers time and pet name. It detects conflicts based on time and pet name. If two tasks are scheduled for the same pet within 15 minutes of each other, or if their durations overlap, then the scheduler flags a conflict.

Constraints that matter most are time and pet name because the same pet can't be in two places at once. So if two tasks are scheduled for the same pet at the same time, that's a conflict. Time is also important because if two tasks are scheduled within 15 minutes of each other, that's likely to be a conflict as well. Not too difficult to see the priority and filter by preferences manually.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler registers a conflict if the tasks have a scheduled time within 15 minutes or they're within one or the other's durations.
This is reasonable because tasks with no duration are likely pretty quick. So if they're 15 minutes before or after one another they're unlikely to be a significant inconvenience. If they're within the duration of each o ther then obviously there's a conflict.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI tools for design brainstorming and debugging. I found it helpful to ask the AI to generate a UML diagram based on my initial design ideas, and then to explain the relationships between classes. I also used AI to help me debug issues with my code, by asking it to review specific functions or methods and suggest improvements.

The prompts or questions that were the most helpful were the most specific ones. For example, asking "Can you generate a UML diagram for a pet scheduling system with classes for Pet, Owner, Task, and Scheduler?" was more helpful than a more general prompt like "Can you help me design a pet scheduling system?" The specific prompt helped the AI understand exactly what I was looking for and provided a more targeted response.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I did not accept the AI's initial suggestion for the test cases because it suggested testing in a way that my design wasn't intended to work.

I evaluated and verified the AI's suggestions by comparing them to my design and the intended functionality of the system. I also considered whether the suggested tests were relevant and would effectively verify the correctness of the system.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

1. Adding a pet to an owner and verifying that the pet is in the owner's list of pets. This is important because it verifies that the add_pet method works correctly and that the relationship between owner and pet is established.
2. Adding a task to a pet and verifying that the task is in the pet's list of tasks. This is important because it verifies that the add_task method works correctly and that the relationship between pet and task is established.
3. Retrieving tasks for a specific date and verifying that the correct tasks are returned. This is important because it verifies that the retrieve_tasks method works correctly and that the scheduler can aggregate tasks across owners and pets based on date.
4. Detecting conflicts between tasks and verifying that the correct conflicts are identified. This is important because it verifies that the detect_conflicts method works correctly and that the scheduler can identify scheduling issues.
5. Marking a task as complete and verifying that the task's completed attribute is updated. Also that the task is rescheduled if it has a frequency. This is important because it verifies that the mark_complete method works correctly and that task completion status can be tracked.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am fairly confident that the core functionality of the scheduler works correctly based on the tests I have implemented. However, there may be edge cases that I haven't considered or tested yet. If I had more time, I would test edge cases such as:
- Scheduling tasks for multiple pets

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

Probably the overall design and structure of the system. I think I was able to practice each stage of designing an organized system that allows for easy extension and modification in the future. Good practice with object-oriented design and thinking about how to structure a system in a way that allows for flexibility and scalability.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would improve the test coverage to include more edge cases and ensure that all possible scenarios are tested. I would also consider adding more functionality to the system, such as the ability to handle recurring tasks or to integrate with a calendar API for better scheduling and reminders.

Might be a good opportunity to implement Test Driven Development (TDD) to ensure that the design and implementation are closely aligned with the desired functionality from the start.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

One important thing I learned about designing systems is the importance of thinking through the relationships between classes and how they interact with each other. It's crucial to design a system that is organized and modular, so that it's easy to extend and modify in the future. I also learned that when working with AI, it's important to be specific in your prompts and questions to get the most helpful responses.