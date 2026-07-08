from dataclasses import dataclass, field
from typing import List

@dataclass
class Task:
    description: str
    due_time: str
    frequency: str = "Once"  # Added frequency based on new requirements
    is_completed: bool = False

    def mark_complete(self) -> None:
        """Marks the task as finished."""
        self.is_completed = True

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
        """
        Aggregates all pending tasks for all pets belonging to an owner.
        Returns a list of dictionaries to map the task to the specific pet.
        """
        daily_schedule = []
        for pet in owner.get_all_pets():
            for task in pet.get_pending_tasks():
                daily_schedule.append({
                    "pet_name": pet.name,
                    "task": task
                })
        return daily_schedule