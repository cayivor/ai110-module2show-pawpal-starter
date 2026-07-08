from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import List

@dataclass
class Task:
    description: str
    due_time: str              # e.g., "08:00 AM"
    frequency: str = "Once"    # "Once", "Daily", or "Weekly"
    is_completed: bool = False

    def mark_complete(self, current_pet) -> None:
        """Marks the current task as finished. If it's recurring, schedules the next one."""
        self.is_completed = True
        
        if self.frequency.lower() in ["daily", "weekly"]:
            # Calculate the next occurrence time
            days_to_add = 1 if self.frequency.lower() == "daily" else 7
            
            # Create the description for the next occurrence
            next_description = f"{self.description} (Next Occurrence)"
            
            # Spawn the new recurring task copy (uncompleted)
            next_task = Task(
                description=next_description,
                due_time=self.due_time,
                frequency=self.frequency,
                is_completed=False
            )
            
            # Automatically append it back to the pet's task list
            current_pet.add_task(next_task)

@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Assigns a new task to the pet."""
        self.tasks.append(task)

    def get_pending_tasks(self) -> List[Task]:
        """Returns all tasks that are not yet completed."""
        return [task for task in self.tasks if not task.is_completed]

@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Adds a new pet to the owner's profile."""
        self.pets.append(pet)

    def get_all_pets(self) -> List[Pet]:
        """Returns all pets owned by this owner."""
        return self.pets

@dataclass
class Scheduler:
    owners: List[Owner] = field(default_factory=list)

    def register_owner(self, owner: Owner) -> None:
        """Registers a new owner in the system."""
        self.owners.append(owner)

    def get_daily_schedule(self, owner: Owner) -> List[dict]:
        """Aggregates all pending tasks for all pets belonging to an owner."""
        daily_schedule = []
        for pet in owner.get_all_pets():
            for task in pet.get_pending_tasks():
                daily_schedule.append({
                    "pet_name": pet.name,
                    "task": task
                })
        return daily_schedule

    def sort_by_time(self, schedule: List[dict]) -> List[dict]:
        """Sorts a schedule chronologically using a lambda function and datetime."""
        def parse_time(item):
            time_str = item["task"].due_time
            # Handle edge cases where a time wasn't strictly formatted
            if time_str.lower() == "flexible" or time_str == "":
                return datetime.strptime("11:59 PM", "%I:%M %p") # Push flexible tasks to the end of the day
            try:
                # Convert "08:00 AM" string into a comparable datetime object
                return datetime.strptime(time_str, "%I:%M %p")
            except ValueError:
                return datetime.strptime("11:59 PM", "%I:%M %p")

        # The lambda extracts the parsed time to use as the sorting key
        return sorted(schedule, key=lambda x: parse_time(x))

    def filter_by_pet(self, schedule: List[dict], pet_name: str) -> List[dict]:
        """Returns only tasks belonging to a specific pet."""
        return [item for item in schedule if item["pet_name"].lower() == pet_name.lower()]

    def filter_by_status(self, schedule: List[dict], is_completed: bool) -> List[dict]:
        """Returns tasks based on their completion status."""
        return [item for item in schedule if item["task"].is_completed == is_completed]
    
    def check_for_conflicts(self, daily_schedule: List[dict]) -> List[str]:
        """Scans the schedule for tasks occurring at the exact same time and returns warnings."""
        warnings = []
        time_slots = {}
        
        # Group tasks by their due_time
        for item in daily_schedule:
            time_str = item["task"].due_time
            # Ignore flexible tasks since they don't have a strict time conflict
            if time_str.lower() == "flexible" or time_str == "":
                continue
                
            if time_str not in time_slots:
                time_slots[time_str] = []
            time_slots[time_str].append(item)
            
        # If any time slot has more than 1 task, it's a conflict!
        for time_str, items in time_slots.items():
            if len(items) > 1:
                # Create a readable warning message
                conflict_details = " and ".join([f"{i['pet_name']}'s '{i['task'].description}'" for i in items])
                warnings.append(f"⚠️ CONFLICT WARNING: Double-booked at {time_str} for {conflict_details}")
                
        return warnings